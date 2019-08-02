from LFLpd.drivers.awg520 import AWG
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.alazar import ADC
from LFLpd.tools.datatools import unique_filename
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

#connect to devices
smfR = SMF("TCPIP::192.168.1.121::INSTR")
smfQ = SMF("TCPIP::192.168.1.122::INSTR")
awg = AWG("GPIB0::6::INSTR")
adc = ADC()

#define parameters
#smfRlevel = -10 # dBm
#smfQlevel = 0 # dBm
qubitFreq = 3.93029 #GHz
resFreq = 7.3 #GHz

#start readout tone generator
smfR.set_freq(resFreq)
smfR.set_level(smfRLevel)
smfR.RF_ON()

#start qubit spectroscopy tone sweep for 2GHz range at 1MHz step
smf.display_update(0)
smf.configure_freq_sweep(qubitFreq-1,qubitFreq+1,1,"MHz",15,"ms")
smf.configure_trig_freq_sweep("EXT","STEP")
smf.set_level(smfQLevel)
smf.RF_ON()
smf.q("*OPC?")
