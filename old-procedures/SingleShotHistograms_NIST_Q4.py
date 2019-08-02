import pickle
import numpy as np
import matplotlib.pyplot as plt

# parameters
nSkipTime = 1.5 # microseconds
nAvgTime = 14.5 # microseconds
nBins = 80 # number of bins for histogram

f = open(r'E:\rawData\LongTracesNIST_Q4.pkl', 'rb')
d = pickle.load(f)
f.close()

data = d.reshape((7632,5,8192))

iSkip = int(500*nSkipTime)
iAvg = int(500*nAvgTime)

fAvg = [np.mean(data[i,j,iSkip:iSkip+iAvg]) for j in range(5) for i in range(7632)]

fig, axs = plt.subplots(2)
fig.suptitle('Single Shot Averaging Time: {} microseconds'.format(nAvgTime))
axs[0].plot(fAvg[0:200],'+')
axs[1].hist(fAvg, bins=nBins)

plt.show()
