import matplotlib.pyplot as plt
import numpy as np

filename = "E:/rawData/Sinc.csv"   #full file path

data = np.genfromtxt(filename, delimiter = ',',skip_header=1,names=['V','t'])

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(data['t'],data['V'])

plt.show()
