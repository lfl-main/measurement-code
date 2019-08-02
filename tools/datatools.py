'''Collection of tools for processing and analyzing data.
Contributors: James Farmer
'''


import numpy as np
import struct
import os
from time import strftime
from pandas import DataFrame


def bin2csv(filename, saveto = "E:/rawData/"):
    '''Converts the binary data file as input and returns a .csv file with usable data. - JF '''
    drive, path = os.path.splitdrive(filename)
    path,file = os.path.split(path)
    newfile = saveto + file.strip('.bin') + ".csv"
    DATA = np.fromfile(filename,dtype=np.uint16)
    DATA = (DATA - 2047.5) * 0.4/2047.5
    if os.path.exists(filename.strip('.bin') + ".txt"):
        with open(filename.strip('.bin') + ".txt",'r') as f:
            (date,channels,duration,samplerate) = f.read().splitlines()
        if channels.strip("Channels: ") == "AB":
            DATA = [DATA[ind::2] for ind in range(2)]
            TIME = [i/float(samplerate.strip('Samples per second: ')) for i in range(len(DATA[0]))]
            DataFrame(np.column_stack((DATA[0],DATA[1],TIME))).to_csv(newfile,index=False,header=("CH A (Volts)","CH B (Volts)","Time (micro-s)"))
        else:
            TIME = [i/float(samplerate.strip('Samples per second: ')) for i in range(len(DATA))] 
            DataFrame(np.column_stack((DATA,TIME))).to_csv(newfile,index=False,header=("Voltage (Volts)","Time (micro-s)"))
    else:
        print('Accompanying text file is not in the directory.')
    
def datafromcsv(filename):
    '''returns a numpy array of float values representing voltage and time.
       One column can be accessed by calling the label: data['V'] or data['t']'''
    with open(filename) as f:
        if f.readline().count(',') == 1:
            labels = ['V','t']
        elif f.readline().count(',') == 2:
            labels = ['A','B','t']
        else:
            print('File is not 2 or 3 columns')
            return ValueError
    D = np.genfromtxt(filename,  delimiter = ',',skip_header=1,names=labels)
    return D
    
def unique_filename(directory,prefix,ext):
    '''Generates a unique, date stamped filename in the specified directory
       with the given prefix and extension'''
    i = 1
    while os.path.exists("%s%s%s_%.f.%s" % 
                         (directory,prefix,strftime("%Y-%m-%d"),i,ext)):
        i += 1
    fname = "%s%s%s_%.f.%s" % (directory,prefix,strftime("%Y-%m-%d"),i,ext)
    return fname
    
def plot_flux_tuning(dataFile,real_imag,fpoints,Istart,Istop,Ipoints,save=True):
    '''imports from flux spectroscopy csv file and plots as a 2D contour.
       real_imag MUST be exactly 'real' or 'imag', case sensitive.
       fpoints is number of points in frequency sweep. Istart/Istop is initial/final biasing current (mA).
       Ipoints is number of points in current sweep. - JF'''
    import matplotlib.pyplot as plt
    data = np.fromfile(dataFile).reshape(Ipoints,fpoints,3)
    Y = np.linspace(Istart,Istop,Ipoints)
    if real_imag == 'real':
        Z = data[:,:,0]
    elif real_imag == 'imag':
        Z = data[:,:,1]
    else:
        return ValueError
    plt.contourf(data[0,:,2],Y,Z,100)
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Bias Current (mA)')
    plt.title('Transmon Frequency Flux Tuning')
    if save:
        plt.savefig(dataFile.strip('.csv')+'.png')
    plt.show()
    
def PSD(dBm,BW):
    '''compute the noise density in dBm/Hz from dBm power and bandwidth(Hz) read off spectrum analyzer'''
    return dBm - 10*np.log10(BW)
def totalNoisePower(PSD,BW):
    '''compute the total noise power in dBm, given the power spectral density in dBm/Hz and the bandwidth in Hz'''
    return PSD + 10*np.log10(BW)

              
### add a function to generate a specified waveform (pulse, gaussian, lorentz, etc.)
### add sweeping functionality
### the sweeped data should be passed into a function once, not call a function each value


#this doesn't really do what I want it to. It serves no purpose but to select the type
    # type of waveform, which we could do ourselves just by calling that function.
#def generate_sweep_arrays(self, wfmtype, parameter):
    #if wfmtype == 'something':
        #generate_something(parameter)

# want to be able to select a waveform type and a parameter to sweep, then pass that
# into a waveform generating function.

# It seems like there's no point in having a function that lets us select the waveform type
# Instead, maybe all the waveform generating functions should be moved to their own file,
# and I can just create a bunch of functions to sweep each parameter for each waveform type

# It should be easy to modify the root waveform generator to sweep each parameter.
    
