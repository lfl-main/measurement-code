from LFLpd.drivers.VNA import VNA
from LFLpd.drivers.smf100a import SMF
from LFLpd.tools.datatools import unique_filename
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

# connect to devices
smf = SMF("TCPIP::192.168.1.121::INSTR", reset=True)
vna = VNA("GPIB1::16::INSTR")

# define parameters
vnaLevel = 0  # dBm
vnaFreq = 5.9553 # GHz
smfLevel = -10  # dBm
smfDwell = 20   # ms
startFreq = 7.7   # GHz
stopFreq = 7.9 # GHz
stepFreq = 100    # kHz
numpoints = int(1+(stopFreq - startFreq)/(stepFreq*1e-6))



# set up VNA for continuous wave and triggering the smf
vna.setupQubitSpectroscopy(npoints=numpoints,freq=vnaFreq,power=vnaLevel)

# set up signal generator for freq sweep triggered by VNA
smf.display_update(1)
smf.configure_freq_sweep(startFreq,stopFreq,stepFreq,"kHz",smfDwell,"ms")
smf.configure_trig_freq_sweep("EXT","STEP")
smf.set_level(smfLevel)
smf.RF_ON()
smf.q("*OPC?")

#Take measurement
data = vna.qubitSpectroscopyMeas()
smf.RF_OFF()
vna.inst.close()
smf.inst.close()

#convert Smith to real and imaginary
f=np.linspace(startFreq,stopFreq,num=numpoints)
y=data.split(",")
real=[float( y[2*i]) for i in range(int(len(y)/2))]
imag=[float( y[2*i+1]) for i in range(int(len(y)/2))]

#save real and imaginary data
fname = unique_filename("E:/rawData/VNAmeasurements/","qubitSpectroscopy_{}dBm".format(smfLevel),"csv")
DataFrame(np.column_stack((real,imag,f))).to_csv(
    fname,index=False,header=("Real","Imaginary","Frequency (GHz)"))

#plot and save figure
plt.figure()

rmin = np.amin(real)
rmax = np.amax(real)
rscale = 0.1*(rmax-rmin)
imin = np.amin(imag)
imax = np.amax(imag)
iscale = 0.1*(imax-imin)


ax1 = plt.subplot(211)
#plt.xlabel('Frequency (GHz)')
plt.ylabel('Real')
plt.ylim(rmin-rscale,rmax+rscale)
plt.plot(f,real, label="{} dBm".format(smfLevel))
#plt.plot(f,realm, label="-30 dBm")
plt.legend()

ax2 = plt.subplot(212)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Imaginary')
plt.ylim(imin-iscale,imax+iscale)
plt.plot(f,imag, label="{} dBm".format(smfLevel))
#plt.plot(f,imagm, label="-30 dBm")
plt.legend()

plt.savefig(fname.strip('.csv')+'.png')

plt.show()




