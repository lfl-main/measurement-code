from LFLpd.drivers.VNA import VNA
from LFLpd.tools.datatools import unique_filename
import matplotlib.pyplot as plt
from time import sleep
from pandas import DataFrame
import numpy as np
x=VNA(address='GPIB1::16::INSTR')

# parameters
level = 18
fstart = 5.30180 #GHz
fstop = 6.30180 #GHz


mem = x.s21memory()
ym = mem.split(",")
realm=[float( ym[2*i]) for i in range(int(len(ym)/2))]
imagm=[float( ym[2*i+1]) for i in range(int(len(ym)/2))]

results=x.S21meas(power=level,start=fstart,stop=fstop)

f=np.linspace(fstart,fstop,num=201)
y=results.split(",")
real=[float( y[2*i]) for i in range(int(len(y)/2))]
imag=[float( y[2*i+1]) for i in range(int(len(y)/2))]

fname = unique_filename("E:/rawData/VNAmeasurements/","Punchout","csv")
DataFrame(np.column_stack((real,imag,realm,imagm,f))).to_csv(
    fname,index=False,header=("Real","Imaginary","Real Memory","Imaginary Memory","Frequency (GHz)"))

plt.figure()

rmin = np.amin(real) - 0.2*abs(np.amin(real))
rmax = np.amax(real) + 0.2*abs(np.amax(real))
imin = np.amin(imag) - 0.2*abs(np.amin(imag))
imax = np.amax(imag) + 0.2*abs(np.amax(imag))

ax1 = plt.subplot(211)
#plt.xlabel('Frequency (GHz)')
plt.ylabel('Real')
plt.ylim(rmin,rmax)
plt.plot(f,real, label="{} dBm".format(level))
plt.plot(f,realm, label="-30 dBm")
plt.legend()

ax2 = plt.subplot(212)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Imaginary')
plt.ylim(imin,imax)
plt.plot(f,imag, label="{} dBm".format(level))
plt.plot(f,imagm, label="-30 dBm")
plt.legend()

plt.savefig(fname.strip('.csv')+'.png')

plt.show()


x.disconnect()
