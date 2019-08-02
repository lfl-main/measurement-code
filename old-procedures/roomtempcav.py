from LFLpd.drivers.VNA import VNA
from LFLpd.tools.datatools import unique_filename
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

vna = VNA("GPIB1::16::INSTR")

startFreq = float(vna.q("SENS1:FREQ:STAR?"))
stopFreq = float(vna.q("SENS1:FREQ:STOP?"))


data = vna.Smeas('S21')
f=np.linspace(startFreq,stopFreq,num=201)
y=data.split(",")
real=[float( y[2*i]) for i in range(int(len(y)/2))]
imag=[float( y[2*i+1]) for i in range(int(len(y)/2))]
fname = unique_filename("E:/rawData/VNAmeasurements/","RoomTempCavity","csv")
DataFrame(np.column_stack((real,imag,f))).to_csv(
    fname,index=False,header=("Real","Imaginary","Frequency (GHz)"))
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
plt.plot(f,real)
#plt.plot(f,realm, label="-30 dBm")
plt.legend()

ax2 = plt.subplot(212)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Imaginary')
plt.ylim(imin-iscale,imax+iscale)
plt.plot(f,imag)
#plt.plot(f,imagm, label="-30 dBm")
plt.legend()

plt.savefig(fname.strip('.csv')+'.png')

plt.show()
