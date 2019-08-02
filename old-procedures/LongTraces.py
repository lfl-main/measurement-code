import Labber
import numpy as np
import os
import pickle
from time import clock
import h5py

#parameters
nTraces = 200000
nSamplesPerTrace = 28672
nRecordsPerAcq = 200

# create dataFile
#dataFileName = r"E:\rawData\NIST_Q4_LongerTraces_withNoDelay.bin"
#dataFile = open(os.path.join(os.path.dirname(__file__),dataFileName),'wb')

#create hdf5 file
hdf5_store = h5py.File(r'E:\rawData\NIST_Q4_LongerTraces_withNoDelay_3.hdf5','a')

# connect to labber and digitizer
client = Labber.connectToServer('Localhost')
dig = client.connectToInstrument('AlazarTech Digitizer',dict(interface='Other', address='1'))
dig.startInstrument()

# calculate some parameters
nIter = int(nTraces/nRecordsPerAcq)
start = clock()
print('number of iter:',nIter)

# Create the pickle file
#f = open(r'E:\rawData\NIST_Q4_LongerTraces_withNoDelay.pkl','wb')


data = hdf5_store.create_dataset('data', (nIter, nRecordsPerAcq*nSamplesPerTrace))

try:
    for i in range(nIter):
        d1 = dig.getValue('Ch1 - Data')['y']
        #d1.tofile(dataFile)
        #pickle.dump(d1,f)
        data[i,] = d1
        if i<10:
            print(i)
            print(clock()-start)

finally:
    #dataFile.close()
    #f.close()
    hdf5_store.close()
    client.close()
    
