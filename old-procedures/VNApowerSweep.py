from LFLpd.drivers.VNA import VNA
import matplotlib.pyplot as plt
import numpy as np
import Labber
from time import sleep

v = VNA("GPIB1::16::INSTR")

#parameters
#qPower = 10
#frequencies = np.linspace(5,6,4000)
LogFileName = 'NIST_VNA_SingleShotPunchout'
vPower = np.linspace(-13,7,101)
tSweep = float(v.q("SENS:SWE:TIME?"))  # Find the total time of the VNA sweep

#prepare Labber
lStep = [dict(name='VNA Power', unit='dBm', values=vPower)]
lLog = [dict(name = 'VNA Signal', unit = 'mW',  complex=True, vector=True,
             x_name='Time',x_unit='ms')]
f = Labber.createLogFile_ForData(LogFileName,lLog,step_channels=lStep)

for p in vPower:
    v.w("SOUR1:POW1 {}".format(p)) # sets the RF power level
    v.q("*OPC?")
    sleep(tSweep)
    #get data
    sData = v.getTrace()
    lData = sData.split(',')
    vData = np.array([float(lData[i]) for i in range(len(lData))], dtype='>f')
    nPts = int(len(vData)/2)
    mC = vData.reshape((nPts,2))
    vComplex = mC[:,0] + 1j*mC[:,1]
    #Save the log file
    trace_dict = Labber.getTraceDict(vComplex,x0=0, x1=tSweep)
    data = {'VNA Signal': trace_dict}
    f.addEntry(data)


#plt.figure()

#plt.plot(abs(vComplex))
#plt.show()

v.disconnect()

