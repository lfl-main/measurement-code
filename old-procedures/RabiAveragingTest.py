
from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.alazar import ADC
from LFLpd.tools.wfmtools import generateRabiPulses
from LFLpd.tools.datatools import datafromcsv, bin2csv
from multiprocessing.pool import ThreadPool
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

#define parameters
acquisition_length = 2e-7 #seconds
smfLevel = 0 #dBm
qubitFreq = 6.61 #GHz
resFreq = 5.59129 #GHz
pool = ThreadPool(processes=1)

#initiate hardware
awg = AWG("GPIB0::3::INSTR")
smfQ = SMF("TCPIP::192.168.1.121::INSTR")
smfR = SMF("GPIB0::1::INSTR")
adc = ADC()

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

#full loop through multiple durations
rabiV = []
for tau in range(50,3001,50):
    #generate waveform and load to AWG
    f1,f2 = generateRabiPulses(tstart = 25, width1 = tau, width2 = 500, duration = 4000)
    fname1 = awg.send_waveform(f1)
    fname2 = awg.send_waveform(f2)
    awg.load_waveform(1,fname1)
    awg.load_waveform(2,fname2)
    awg.signal_level(1,1)
    awg.signal_level(2,1)
    awg.set_mode("TRIG")
    awg.enable_output(1)
    awg.enable_output(2)
    #measure an ensemble of experiments
    avgV = []
    for i in range(10):
        adcWorker = pool.apply_async(adc.startTriggeredCapture,
                                     (acquisition_length,),{'channel':'AB','returnfname':True})
        sleep(0.5)
        awg.force_trigger()
        sleep(0.1)
        datafile = adcWorker.get()
        bin2csv(datafile)
        data = datafromcsv(datafile.strip('.bin') + '.csv')
        V = np.sqrt(data['A']**2 + data['B']**2)
        avgV.append(np.mean(V))
    rabiV.append(np.mean(avgV))
    awg.disable_output(1)
    awg.disable_output(2)

#disable outputs
sleep(0.5)
smfQ.RF_OFF()
smfR.RF_OFF()

#plot data
plt.figure()
plt.title('Rabi Test')

#for dual channel acquisitions, to plot single channel, eliminate second subplot and change data['A'] to data['V']

ax1 = plt.subplot(111)
plt.xlabel('pulse duration (ns)')
plt.ylabel('average V')
ax1.plot(range(50,3001,50),rabiV)

plt.show()


