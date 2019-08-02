import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import tkinter as t
import h5py


def update():
    iSkip = int(nSampleRate*float(sSkip.get()))
    iAvg = int(nSampleRate*float(sAvg.get()))
    vAvg = [np.mean(hd['data'][i,j*nSamples+iSkip:j*nSamples+iSkip+iAvg])
            for j in range(nTracesPerAcq) for i in range(int(sIter.get()))]
    l1.set_ydata(vAvg[0:200])
    axs[1].cla()
    axs[1].hist(vAvg, bins=nBins)
    canvas.draw()


# parameters
nSkipTime = 1.5 # microseconds
nAvgTime = 14.5 # microseconds
nSampleRate = 500 # MegaSample/second
nBins = 80 # number of bins for histogram
nSamples = 28672  # number of samples for a single trace
nTraces = 200000
nTracesPerAcq = 200

nIterMax = int(nTraces/nTracesPerAcq)

# convert times to indices
iSkip = int(nSampleRate*nSkipTime)
iAvg = int(nSampleRate*nAvgTime)

# get data and reshape it into an array of individual traces
#data = np.fromfile(r'E:\rawData\NIST_Q4_LongerTraces.bin')
#nTraces = int(len(data)/nSamplesPerTrace)
#data = data.reshape((nTraces,nSamplesPerTrace))

# open hdf5 file
hd = h5py.File(r'E:\rawData\NIST_Q4_LongerTraces_withNoDelay_3.hdf5','r')


# Calculate the averaged data
vAvg = [np.mean(hd['data'][i,j*nSamples+iSkip:j*nSamples+iSkip+iAvg]) for j in range(nTracesPerAcq) for i in range(100)]

# Start GUI
m = t.Tk()
m.wm_title("Single Shot Averaging")

fig, axs = plt.subplots(2)
l1, = axs[0].plot(vAvg[0:200],'+')
axs[1].hist(vAvg, bins=nBins)

canvas = FigureCanvasTkAgg(fig,master=m)
canvas.draw()
canvas.get_tk_widget().pack(side=t.TOP,fill=t.BOTH,expand=1)

toolbar = NavigationToolbar2Tk(canvas,m)
toolbar.update()
canvas.get_tk_widget().pack(side=t.TOP,fill=t.BOTH,expand=1)

# make entries
f1 = t.Frame(m)
lSkip =  t.StringVar()
lSkip.set("Skip Time (us)")
lSkipDir = t.Label(f1,textvariable=lSkip)
lSkipDir.pack(side='left')
sSkip = t.StringVar(None,value=str(nSkipTime))
eSkip = t.Entry(f1,textvariable=sSkip)
eSkip.pack(side='right')
f1.pack(anchor='e', fill='both', expand=1)

f2 = t.Frame(m)
lAvg =  t.StringVar()
lAvg.set("Averaging Time (us)")
lAvgDir = t.Label(f2,textvariable=lAvg)
lAvgDir.pack(side='left')
sAvg = t.StringVar(None,value=str(nAvgTime))
eAvg = t.Entry(f2,textvariable=sAvg)
eAvg.pack(side='right')
f2.pack(anchor='e',fill='both',expand=1)

f3 = t.Frame(m)
lIter =  t.StringVar()
lIter.set("# of 200 trace blocks to include (max 1000)")
lIterDir = t.Label(f3,textvariable=lIter)
lIterDir.pack(side='left')
sIter = t.StringVar(None,value=str(100))
eIter = t.Entry(f3,textvariable=sIter)
eIter.pack(side='right')
f3.pack(anchor='e',fill='both',expand=1)

bUpdate = t.Button(m,text='Update',command=update)
bUpdate.pack()
#axcolor = 'lightgoldenrodyellow'
#axSkip = plt.axes([0.25,0.1,0.65,0.03],facecolor=axcolor)
#axAvg = plt.axes([0.25,0.15,0.65,0.03],facecolor=axcolor)
#bSkipTime = TextBox(axSkip, 'Skip (us)', 0.3, 5, initial=str(nSkipTime))
#bAvgTime = TextBox(axAvg,'Average (us)', 2, 50, initial=str(nAvgTime))



#sSkipTime.on_changed(update)
#sAvgTime.on_changed(update)

m.mainloop()
    
