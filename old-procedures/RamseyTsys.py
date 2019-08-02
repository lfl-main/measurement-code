import Labber
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sc

# open log files
fR = Labber.LogFile(r'G:\Shared drives\LFL\Labber\Data\2019\07\Data_0703\Ramsey_vs_readoutPower_Smaller_3.hdf5')
fS = Labber.LogFile(r'G:\Shared drives\LFL\Labber\Data\2019\07\Data_0704\SNR_vs_readoutPower.hdf5')
fP = Labber.LogFile(r'G:\Shared drives\LFL\Labber\Data\2019\07\Data_0704\powerIn_vs_readoutPower.hdf5')

# Get Log File info
##print('Number of entries:', fR.getNumberOfEntries())
##
##print('Step channels:')
##step_channels = fR.getStepChannels()
##for channel in step_channels:
##    print(channel['name'])
##
##print('Log channels:')
##log_channels = fR.getLogChannels()
##for channel in log_channels:
##    print(channel['name'])
##
##print('User:', fR.getUser())
##print('Tags:', fR.getTags())
##print('Project:', fR.getProject())
##print('Comment:', fR.getComment())


# Get Ramsey data and average
Rdata = np.real(fR.getData(name='Ch 1 - Value')).reshape(26,500,101)
Rdata = np.mean(Rdata,axis=1)
print(np.shape(Rdata))
step_channels = fR.getStepChannels()
tR = step_channels[0]['values']

# Get SNR and average
Sdata = fS.getData().reshape(26,40,401)
Sdata = 10**(Sdata/10.)
Sdata = np.mean(Sdata,axis=1)
Sdata = 10*np.log10(Sdata)
print(np.shape(Sdata))

# Get power and average
Pdata= fP.getData().reshape(26,10,401)
Pdata = 10**(Pdata/10.)
Pdata = np.mean(Pdata,axis=1)
Pdata = 10*np.log10(Pdata)
print(np.shape(Pdata))

# save to matlab file for curve fitting
sc.savemat(r'E:\MATLAB\2019-07\RamseyTsysData.mat',mdict={'Data':Rdata,'Time':tR,'Power':Pdata,'SNR':Sdata})

##for i in range(26):
##    plt.figure(i+1)
##    plt.plot(Rdata[i,:])
##    plt.show()

##Rdata = fR.getData().reshape(26,500,101)
##Rdata = np.mean(Rdata,axis=1)
##
##print(np.shape(Rdata))
##plt.plot(tR,Rdata[1,:])
##plt.show()

