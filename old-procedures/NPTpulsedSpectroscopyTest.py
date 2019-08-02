from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.alazar import ADC
from LFLpd.drivers.keithley2400 import K2400SM
from LFLpd.tools.wfmtools import generateSpectroscopyPulses
from LFLpd.tools.datatools import datafromcsv, bin2csv
from multiprocessing.pool import ThreadPool
from time import sleep
import matplotlib.pyplot as plt
import os.path as path
import numpy as np


pool = ThreadPool(processes=1)


#define parameters
acquisition_length = 2e-7 #seconds
Ibias = 38 * 1e-3 # mA
cavityTonePower = -117.5 + 120 #dBm
qubitTonePower = -105 + 100 #dBm
qubitPulseLength = 500 # ns
readPulseLength = 500 # ns
resFreq = 5.8018 # GHz
qubitFreq = 7.8 #GHz
startFreq = 7.7 # GHz
stopFreq = 7.9 # GHz
stepFreq = 100 # kHz
numpoints = int(1+(stopFreq - startFreq)/(stepFreq*1e-6))
smfDwell = 2 # ms



# check if waveforms already exists, if not, make them
f1 = "E:/waveforms/Spectroscopy_Ch1_{}ns_{}ns.wfm".format(qubitPulseLength,readPulseLength)
f2 = "E:/waveforms/Spectroscopy_Ch2_{}ns_{}ns.wfm".format(qubitPulseLength,readPulseLength)
if not (path.exists(f1) and path.exists(f2)):
    generateSpectroscopyPulses(width1=qubitPulseLength,width2=readPulseLength)
    sleep(1)


# initiate hardware
awg = AWG("GPIB0::3::INSTR")
smfQ = SMF("TCPIP::192.168.1.121::INSTR")
smfR = SMF("GPIB0::1::INSTR")
ksm = K2400SM("GPIB1::24::INSTR")
adc = ADC()


# start cavity tone
smfR.set_freq(resFreq)
smfR.set_level(cavityTonePower)
smfR.RF_ON()

# set up qubit spectroscopy tone
smfQ.display_update(0)
smfQ.configure_freq_sweep(startFreq,stopFreq,stepFreq,"kHz",smfDwell,"ms")
smfQ.configure_trig_freq_sweep("EXT","STEP")
smfQ.set_level(qubitTonePower)
smfQ.RF_ON()
smfQ.q("*OPC?")


# set up SourceMeter for bias current
ksm.sourceFunction('i')
ksm.setSourceRange('i',0.1)
ksm.selectMeasureFN('v')
ksm.setMeasurementRange('v',0.01)
ksm.setComplianceLevel('v',0.08)
ksm.setLevel('i',Ibias)
ksm.outputState('on')


#configure ADC
adc.configureClock(MS_s=1000)
adc.configureTrigger()

# send and load waveform to AWG
fname1 = awg.send_waveform(f1)
fname2 = awg.send_waveform(f2)
awg.load_waveform(1,fname1)
awg.load_waveform(2,fname2)
awg.signal_level(1,1)
awg.signal_level(2,1)
awg.set_mode("TRIG")
awg.enable_output(1)
awg.enable_output(2)

samples = 128
adcWorker = pool.apply_async(adc.startTriggeredCapture,(samples,),
                             {'channel':'AB','returnfname':True})
sleep(0.3)

for i in range(numpoints):
    awg.force_trigger()
    sleep(0.002)

# disable outputs
#adc.board.abortAsyncRead()
awg.disable_output(1)
awg.disable_output(2)
smfQ.RF_OFF()
smfR.RF_OFF()
ksm.outputState('off')

dataFile = adcWorker.get()

bin2csv(dataFile)
data = datafromcsv(dataFile.strip('.bin') + '.csv')

print(len(data['A']))
print(len(data['B']))
print(data['A'][0])

plt.figure()
plt.title('Pulsed Spectroscopy')
ax1 = plt.subplot(211)
plt.xlabel('Frequency (GHz)')
plt.ylabel('I')
#ax1.plot(np.linspace(startFreq,stopFreq,numpoints),




