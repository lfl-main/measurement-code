from LFLpd.drivers.VNA import VNA
from LFLpd.drivers.smf100a import SMF
import numpy as np
import Labber

# Parameters
fStart = 5.4 #GHz
fStop = 5.7 #GHz
fStep = 100 #kHz
pQubit = [-16,-13,-10,-7] #dBm
fResonator = 7.070035 #GHz
pResonator = -18 #dBm

# Generate Log File Name
LogFileName = 'NIST_R4_{}Ghz_{}dBm_{}-{}GHz'.format(fResonator,pResonator,fStart,fStop)

# Calculate constants
nPts = int(0.5+((fStop - fStart)/(fStep*1e-6))) + 1
print("There are {} points in each sweep".format(nPts))
print("For {} sweeps, I estimate this will take more than {} s".format(len(pQubit),len(pQubit)*nPts/50.))

# Connect to instruments
v = VNA("GPIB1::16::INSTR")
s = SMF("TCPIP::192.168.1.122::INSTR")

# Prepare VNA for spectroscopy
v.setupQubitSpectroscopy(npoints=nPts,freq=fResonator,power=pResonator)

# set up signal generator for freq sweep triggered by VNA
s.display_update(1)
s.configure_freq_sweep(fStart,fStop,fStep,"kHz")
s.configure_trig_freq_sweep("EXT","STEP")
s.RF_ON()
s.execute_freq_sweep()

# Prepare the Labber Log File with list of dictionaries defining step and log channels
lStep = [dict(name='Qubit Tone Power', unit='dBm', values=np.array(pQubit))]
lLog = [dict(name = 'VNA Signal', unit = 'mW',  complex=True, vector=True,
             x_name='Qubit Tone Frequency',x_unit='GHz')]
f = Labber.createLogFile_ForData(LogFileName,lLog,step_channels=lStep)

# Check that instruments are ready
v.q("*OPC?")
s.q("*OPC?")

# Run sweeps
for p in pQubit:
    # Update qubit tone power
    s.set_level(p)
    s.w("SWE:RES") #reset the sweep to starting point, just in case
    s.q("*OPC?")

    # Get and convert VNA data
    sData = v.qubitSpectroscopyMeas()
    lData = sData.split(',')
    vData = np.array([float(lData[i]) for i in range(len(lData))], dtype='>f')
    mC = vData.reshape((nPts,2))
    vComplex = mC[:,0] + 1j*mC[:,1]

    # save data to log file
    trace_dict = Labber.getTraceDict(vComplex,x0=fStart, x1=fStop)
    data = {'VNA Signal': trace_dict}
    f.addEntry(data)

# Close instrument connections
v.inst.close()
s.inst.close()
    

