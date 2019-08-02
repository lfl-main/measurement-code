import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

# parameters
nSkipTime = 1.5 # microseconds
nAvgTime = 14.5 # microseconds
nSampleRate = 500 # MegaSample/second
nBins = 80 # number of bins for histogram
nSamplesPerTrace = 28672  # number of samples for a single trace

# convert times to indices
iSkip = int(nSampleRate*nSkipTime)
iAvg = int(nSampleRate*nAvgTime)

# get data and reshape it into an array of individual traces
data = np.fromfile(r'E:\rawData\NIST_Q4_LongerTraces.bin')
nTraces = int(len(data)/nSamplesPerTrace)
data = data.reshape((nTraces,nSamplesPerTrace))

# Calculate the averaged data
fAvg = [np.mean(data[i,iSkip:iSkip+iAvg]) for i in range(nTraces)]


fig, axs = plt.subplots(2)
plt.subplots_adjust(bottom=0.25)
fig.suptitle('Single Shot Averaging Time: {} microseconds'.format(nAvgTime))
l1, = axs[0].plot(fAvg[0:200],'+')
axs[1].hist(fAvg, bins=nBins)

# make sliders
axcolor = 'lightgoldenrodyellow'
axSkip = plt.axes([0.25,0.1,0.65,0.03],facecolor=axcolor)
axAvg = plt.axes([0.25,0.15,0.65,0.03],facecolor=axcolor)

bSkipTime = TextBox(axSkip, 'Skip (us)', 0.3, 5, initial=str(nSkipTime))
bAvgTime = TextBox(axAvg,'Average (us)', 2, 50, initial=str(nAvgTime))

def update(val):
    Skip = int(nSampleRate*sSkipTime.val)
    Avg = int(nSampleRate*sAvgTime.val)
    vAvg = [np.mean(data[i,Skip:Skip+Avg]) for i in range(nTraces)]
    l1.set_ydata(vAvg[0:200])
    axs[1].cla()
    axs[1].hist(vAvg, bins=nBins)
    fig.canvas.draw_idle()

sSkipTime.on_changed(update)
sAvgTime.on_changed(update)

    
plt.show()
    
