from LFLpd.drivers.VNA import VNA
from LFLpd.tools.datatools import unique_filename
import matplotlib.pyplot as plt
from time import sleep
from pandas import DataFrame
import numpy as np
x=VNA(address='GPIB1::16::INSTR')

'''
trigger:
    trigger source: internal
    (we will need external triggering to work with the generator)
    trigger scope: global
    channel trigger state: channel one, continous
sweep:
    sweep time: 185.326 msec
trace: s21
format: phase
freqency start
frequency stop
IF bandwidth
sweep type: linear frequency
trigger: continous
number of points: 201
electrical delay:49.368695 ns
'''
# parameters
level = -25
fstart = 5.85 #GHz
fstop = 6.05 #GHz
numpoints = 401

results=x.S21meas()
x.disconnect()
#print(results)


f=np.linspace(fstart,fstop,num=401)
#print(f)
#print(type(results))
y=results.split(",")
real=[float( y[2*i]) for i in range(int(len(y)/2))]
imag=[float( y[2*i+1]) for i in range(int(len(y)/2))]

#print(len(real))
#print(len(imag))

fname = unique_filename("E:/rawData/VNAmeasurements/","CavityResponse","csv")
DataFrame(np.column_stack((real,imag,f))).to_csv(fname,index=False,header=("Real","Imaginary","Frequency (GHz)"))

plt.figure()
#plt.title(fname)

ax1 = plt.subplot(211)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Real')
plt.ylim(1.2*np.amin(real),1.2*np.amax(real))
plt.scatter(f,real)

ax2 = plt.subplot(212)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Imaginary')
plt.ylim(1.2*np.amin(imag),1.2*np.amax(imag))
plt.scatter(f,imag)


plt.savefig(fname.strip('.csv')+'.png')

plt.show()


x.disconnect()

