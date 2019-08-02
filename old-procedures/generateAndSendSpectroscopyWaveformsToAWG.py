from LFLpd.drivers.awg520 import AWG
from LFLpd.tools.wfmtools import generateSpectroscopyPulses
import os.path as path

# parameters
qubitPulseLength = 1000 # ns
readPulseLength = 1000 # ns
duration=qubitPulseLength + readPulseLength + 200

# check if waveforms already exists, if not, make them
f1 = "E:/waveforms/Spectroscopy_Ch1_{}ns_{}ns.wfm".format(qubitPulseLength,readPulseLength)
f2 = "E:/waveforms/Spectroscopy_Ch2_{}ns_{}ns.wfm".format(qubitPulseLength,readPulseLength)
if not (path.exists(f1) and path.exists(f2)):
    generateSpectroscopyPulses(width1=qubitPulseLength,width2=readPulseLength,duration=duration)
    
(path1, fname1) = path.split(f1)
(path2, fname2) = path.split(f2)

# initiate hardware
awg = AWG("GPIB0::3::INSTR")

# send and load waveform to AWG
if fname1 and fname2 not in awg.q("MMEM:CAT? 'MAIN'"):
    fname1 = awg.send_waveform(f1)
    fname2 = awg.send_waveform(f2)
awg.load_waveform(1,fname1)
awg.load_waveform(2,fname2)
