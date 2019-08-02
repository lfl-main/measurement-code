from LFLpd.drivers.VNA import VNA
from LFLpd.drivers.smf100a import SMF
from LFLpd.drivers.keithley2400 import K2400SM
from LFLpd.tools.datatools import unique_filename, plot_flux_tuning
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

# connect to devices
smf = SMF("TCPIP::192.168.1.121::INSTR")
vna = VNA("GPIB1::16::INSTR")
ksm = K2400SM("GPIB1::24::INSTR")

# define parameters
vnaLevel = -117.5 + 120 # dBm, 120 dB of attenuation between VNA and cavity
vnaFreq = 5.8018 # GHz
numpoints = 4801
smfLevel = -105 + 100  # dBm, 100 dB attenuation between smf and cavity
smfDwell = 20   # ms
startFreq = 6  # GHz
stopFreq = 8.4  # GHz
stepFreq = 500    # kHz
Istart = 15 # mA, the starting current for bias coils
Istop = 50 # mA, the final current for bias coils
Ipoints = 80 # mA, the increment of stepping bias current

# set up VNA for continuous wave and triggering the smf
vna.setupQubitSpectroscopy(npoints=numpoints,freq=vnaFreq,power=vnaLevel)

# set up SourceMeter for bias current
ksm.sourceFunction('i')
ksm.setSourceRange('i',0.1)
ksm.selectMeasureFN('v')
ksm.setMeasurementRange('v',0.01)
ksm.setComplianceLevel('v',0.1)
ksm.setLevel('i',Istart*1e-3)
ksm.outputState('on')

# set up signal generator for freq sweep triggered by VNA
smf.display_update(0)
smf.configure_freq_sweep(startFreq,stopFreq,stepFreq,"kHz",smfDwell,"ms")
smf.configure_trig_freq_sweep("EXT","STEP")
smf.set_level(smfLevel)
smf.RF_ON()
smf.q("*OPC?")

#take measurement
fname = unique_filename("E:/rawData/VNAmeasurements/","fluxBiasedSpectroscopy","csv")
dataFile = open(fname,'wb')
f=np.linspace(startFreq,stopFreq,num=numpoints)
for Ibias in np.round(np.linspace(Istart,Istop,Ipoints),3):
    data = vna.qubitSpectroscopyMeas()
    ksm.setLevel('i',Ibias*1e-3)
    y=data.split(",")
    real=[float( y[2*i]) for i in range(int(len(y)/2))]
    imag=[float( y[2*i+1]) for i in range(int(len(y)/2))]
    np.column_stack((real,imag,f)).tofile(dataFile)

# turn off instrument outputs
ksm.outputState('off')
smf.RF_OFF()
dataFile.close()

# pull data from file, plot it, and save the figure
plot_flux_tuning(fname,'imag',numpoints,Istart,Istop,Ipoints,save=True)

