import pickle
import Labber as l

# Create log file object
fL = l.LogFile(r'G:/Shared drives/LFL/Labber/Data/2019/06/Data_0628/NIST_R4_LongTraces_4.hdf5')

# open file for pickling, be sure to use wb so it writes binary
f = open('LongTracesNIST_Q4.pkl', 'wb')

# get the data from log file as a numpy array
d = fL.getData()

# pickle the numpy array for faster access later
# pickle saves a raw version of a python object
# This lets you access the object later rather than having to reload data into an object
pickle.dump(d,f)

# close file
f.close()
