''' This programs should load a wfm file onto the AWG and 
set up the Alazar card and signal generator with parameters.
Then it should start the AWG wfm which will then trigger the
signal generator to begin a freq sweep. Then, it will trigger the 
Alazar card to record AWG output on channel 1 and signal generator
on channel 2. -JF'''

# TODO
# try triggering the AWG from the alazar IO output.
# tomorrow, I'll try modulating and demodulation with mixers.

from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.alazar import ADC
import threading
from time import sleep

#define parameters
waveform_path = "E:/waveforms/"
waveform_filename = "freehand.wfm"
acquisition_length = 1e-6 # seconds

#create hardware objects
awg = AWG("GPIB0::5::INSTR")
smf = SMF("GPIB0::1::INSTR")
adc = ADC()

#load AWG wfm
awg.send_waveform(waveform_path + waveform_filename)
awg.load_waveform(1,waveform_filename)
awg.signal_level(1,0.6)
awg.set_mode("TRIG")

#start the AWG
awg.enable_output(1)

#prepare alazar card and start a thread to handle data acquisition.
#threading allows the program to continue running while the threaded process is executed.
adc.configureClock()
adc.configureTrigger()
AlazarWorker = threading.Thread(target=adc.startTriggeredCapture,args=(acquisition_length,))
AlazarWorker.start()

#wait for acquisition
sleep(2)

#stop the AWG
awg.disable_output(1)


