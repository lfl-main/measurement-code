'''This procedure should generate a Ramsey pulse waveform with markers,
send it to the AWG, set the SMF to a 6 GHz sine wave, output one waveform
from the AWG, and trigger a capture with Alazar. The recorded signal should 
look exactly like the pi-pulses at the qubit. -JF'''

from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.alazar import ADC
from LFLpd.tools.wfmtools import generateRamseyPulses
from LFLpd.tools.datatools import datafromcsv, bin2csv
from multiprocessing.pool import ThreadPool
import matplotlib.pyplot as plt
from time import sleep

#define parameters
acquisition_length = 1e-6 #seconds
smfLevel = 0 #dBm
qubitFreq = 6.6 #GHz
resFreq = 5.591 #GHz
pool = ThreadPool(processes=1)

#initiate hardware
awg = AWG("GPIB0::3::INSTR")
smfQ = SMF("TCPIP::192.168.1.121::INSTR")
smfR = SMF("GPIB0::1::INSTR")
adc = ADC()

#generate waveform and load to AWG
f1,f2 = generateRamseyPulses(tstart = 25, width1 = 2, width2 = 50, width3 = 400,
                              delay = 100, duration = 1300,
                              m1times = [10,11,12,13,14])
fname1 = awg.send_waveform(f1)
fname2 = awg.send_waveform(f2)
awg.load_waveform(1,fname1)
awg.load_waveform(2,fname2)
awg.signal_level(1,0.8)
awg.signal_level(2,0.8)
awg.set_mode("TRIG")
awg.enable_output(1)
awg.enable_output(2)

#start SMF output
smfQ.set_freq(qubitFreq)
smfQ.set_level(smfLevel)
smfQ.RF_ON()
smfR.set_freq(resFreq)
smfR.set_level(smfLevel)
smfR.RF_ON()

#configure ADC
adc.configureClock(MS_s=1000)
adc.configureTrigger()
adcWorker = pool.apply_async(adc.startTriggeredCapture,
                             (acquisition_length,),{'channel':'AB','returnfname':True})

#trigger AWG and capture with ADC
sleep(1)
awg.force_trigger()

#disable outputs
sleep(0.5)
smfQ.RF_OFF()
smfR.RF_OFF()
awg.disable_output(1)
awg.disable_output(2)

#plot data
datafile = adcWorker.get()
bin2csv(datafile)
data = datafromcsv(datafile.strip('.bin') + '.csv')

plt.figure()
plt.title('Pulses for Ramsey Measurement')

#for dual channel acquisitions, to plot single channel, eliminate second subplot and change data['A'] to data['V']

ax1 = plt.subplot(211)
plt.xlabel('Time (us)')
plt.ylabel('Channel A (V)')
ax1.plot(data['t'],data['A'])

ax2 = plt.subplot(212)
plt.xlabel('Time (us)')
plt.ylabel('Channel B (V)')
ax2.plot(data['t'],data['B'])


plt.show()



