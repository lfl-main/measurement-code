from LFLpd.drivers.VNA import VNA
import matplotlib.pyplot as plt
import numpy as np
import Labber

v = VNA("GPIB1::16::INSTR")

#parameters
qPower = 10
frequencies = np.linspace(5,6,4000)
LogFileName = 'NIST_VNAspectroscopy_7.06982GHz_{}dBm'.format(qPower)

#prepare Labber
lStep = [dict(name='Qubit Tone Power', unit='dBm', values=np.array([qPower,]))]
lLog = [dict(name = 'VNA Signal', unit = 'mW',  complex=True, vector=True,
             x_name='Qubit Tone Frequency',x_unit='GHz')]
f = Labber.createLogFile_ForData(LogFileName,lLog,step_channels=lStep)

#get data
sData = v.getTrace()
lData = sData.split(',')
vData = np.array([float(lData[i]) for i in range(len(lData))], dtype='>f')

#parse header
#i0 = sData.find(b'#')
#nDig = int(sData[i0+1:i0+2])
#nByte = int(sData[i0+2:i0+2+nDig])
#nData = int(nByte/4)
#nPts = int(nData/2)
nPts = int(len(vData)/2)

# get data to numpy array
#vData = np.frombuffer(sData[(i0+2+nDig):(i0+2+nDig+nByte)],dtype='>f', count=nData)
# data is in I0,Q0,I1,Q1,I2,Q2,.. format, convert to complex
mC = vData.reshape((nPts,2))
vComplex = mC[:,0] + 1j*mC[:,1]


#Save the log file
trace_dict = Labber.getTraceDict(vComplex,x0=frequencies[0], x1=frequencies[-1])
data = {'VNA Signal': trace_dict}
f.addEntry(data)


#plt.figure()

#plt.plot(abs(vComplex))
#plt.show()

v.disconnect()
