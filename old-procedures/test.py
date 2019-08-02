#from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.alazar import ADC
from time import sleep
#awg = AWG("GPIB0::3::INSTR")
adc = ADC()
#awg.load_waveform(1,"freehand.wfm")
#awg.signal_level(1,0.6)
#awg.set_mode("CONT")
adc.configureClock(MS_s = 1000)
adc.configureTrigger("A")
#awg.enable_output(1)
adc.startTriggeredCapture(1e-6)
sleep (1e-6)
#awg.disable_output(1)
