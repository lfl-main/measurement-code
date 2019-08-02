'''
This is a set of functions for generating waveforms which can be loaded onto the AWG520.
Contributors: James Farmer
'''

import numpy as np
import struct
import os
from LFLpd.tools.datatools import unique_filename

def wfm2datablock(filename):
    '''Takes a .wfm file location string as input, and returns the contents
       of the file as well as the file name without path.
       example: data, filename = wfm2datablock("E:/waveforms/wave.wfm")
       -JF'''
    from os.path import split, splitdrive
    drive, path = os.path.splitdrive(filename)
    path,file = os.path.split(path)
    with open(filename,'rb') as f:
        content = f.read()
    f.close()
    return content, file
    
def generateRabiPulses(tstart=25,height1=1, height2=1,width1=100,width2=500,duration=1000, clock=1e9, m1times=False, m2times=False ,save=True):
    fname1 = unique_filename("E:/waveforms/","RabiCh1_","wfm")
    fname2 = unique_filename("E:/waveforms/","RabiCh2_","wfm")
    numpoints = int(duration * 1e-9 * clock + 0.5)
    if numpoints < 256 or numpoints > 4194048:
        print("There are too few or too many sample points in the waveform.")
        print("Please check clock and duration to ensure that 256 <= clock*duration <= 4194048")
        return ValueError
    values1 = np.zeros(numpoints,dtype='float32')
    values2 = np.zeros(numpoints,dtype='float32')
    markers1 = np.zeros(numpoints,dtype='int8')
    markers2 = np.zeros(numpoints,dtype='int8')
    width1steps = int(width1*1e-9*clock + 0.5)
    width2steps = int(width2*1e-9*clock + 0.5)
    start = int(tstart*1e-9*clock + 0.5)
    markers1[start+width1steps+71:start+width1steps+74] += 1 #extra indices to eliminate the pre-trigger capture by Alazar
#   try:
#        if m1times:
#            m1index = [int(t*clock*1e-9) for t in m1times]
#            for i in m1index:
#                markers1[i] += 1
#       if m2times:
#            m2index = [int(t*clock*1e-9) for t in m2times]
#           for i in m2index:
#                markers1[i] += 2
                ### This is only putting markers in marker one and 2 for CH1 of AWG. Nothing is going to CH2 ###
#   except IndexError:
#        print('one or more markers are out of range for the duration')
#    except:
#        print('There was an error making the markers')
    if width1steps + width2steps + start >= numpoints:
        print("Duration is too short for given time parameters.")
        return ValueError
    if np.abs(height1) <= 1 and np.abs(height2) <= 1:
        values1[start:start+width1steps] = height1
        values2[start+width1steps:start+width1steps+width2steps] = height2
    else:
        print("height is out of range. Try again with a value between -1 and 1")
        return ValueError
    binvalues1 = b''
    binvalues2 = b''
    for i,v in enumerate(values1):
        binvalues1 += bytes(v) + struct.pack('<B',markers1[i])
    for i,v in enumerate(values2):
        binvalues2 += bytes(v) + struct.pack('<B',markers2[i])
    numbytes1 = str(len(binvalues1)).encode('utf-8')
    numdigits1 = str(len(numbytes1)).encode('utf-8')
    body1 = b'#' + numdigits1 + numbytes1 + binvalues1
    body1 = b'MAGIC 1000\n' + body1 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes2 = str(len(binvalues2)).encode('utf-8')
    numdigits2 = str(len(numbytes2)).encode('utf-8')
    body2 = b'#' + numdigits2 + numbytes2 + binvalues2
    body2 = b'MAGIC 1000\n' + body2 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    if save == True:
        f1 = open(fname1,'wb')
        f1.write(body1)
        f1.close()
        f2 = open(fname2,'wb')
        f2.write(body2)
        f2.close()
        return fname1,fname2
    return fname1,fname2
    
def generateRamseyPulses(tstart=25,height1=1, height2=1, height3=1, width1=100, width2=100, width3=500,
                         delay=200, duration=1000, clock=1e9, m1times=False, m2times=False ,save=True):
    '''Generates 2 .wfm files with 2 pulses for CH1, followed immediately by one long pulse on CH2. - JF'''
    fname1 = unique_filename("E:/waveforms/","RamseyCh1_","wfm")
    fname2 = unique_filename("E:/waveforms/","RamseyCh2_","wfm")
    numpoints = int(duration * 1e-9 * clock + 0.5)
    if numpoints < 256 or numpoints > 4194048:
        print("There are too few or too many sample points in the waveform.")
        print("Please check clock and duration to ensure that 256 <= clock*duration <= 4194048")
        return ValueError
    values1 = np.zeros(numpoints,dtype='float32')
    values2 = np.zeros(numpoints,dtype='float32')
    markers1 = np.zeros(numpoints,dtype='int8')
    markers2 = np.zeros(numpoints,dtype='int8')
    width1steps = int(width1*1e-9*clock + 0.5)
    width2steps = int(width2*1e-9*clock + 0.5)
    width3steps = int(width3*1e-9*clock + 0.5)
    delaysteps = int(delay*1e-9*clock + 0.5)
    start = int(tstart*1e-9*clock + 0.5)
    try:
        if m1times:
            m1index = [int(t*clock*1e-9) for t in m1times]
            for i in m1index:
                markers1[i] += 1
        if m2times:
            m2index = [int(t*clock*1e-9) for t in m2times]
            for i in m2index:
                markers1[i] += 2
    except IndexError:
        print('one or more markers are out of range for the duration')
    except:
        print('There was an error making the markers')
    if width1steps + width2steps + width3steps + delaysteps + start >= numpoints:
        print("Duration is too short for given time parameters.")
        return ValueError
    if np.abs(height1) <= 1 and np.abs(height2) <= 1 and np.abs(height3) <= 1:
        values1[start:start+width1steps] = height1
        values1[start+width1steps+delaysteps:start+width1steps+width2steps+delaysteps] = height2
        values2[start+width1steps+width2steps+delaysteps:start+width1steps+width2steps+delaysteps+width3steps] = height3
    else:
        print("height is out of range. Try again with a value between -1 and 1")
        return ValueError        
    binvalues1 = b''
    binvalues2 = b''
    for i,v in enumerate(values1):
        binvalues1 += bytes(v) + struct.pack('<B',markers1[i])
    for i,v in enumerate(values2):
        binvalues2 += bytes(v) + struct.pack('<B',markers2[i])
    numbytes1 = str(len(binvalues1)).encode('utf-8')
    numdigits1 = str(len(numbytes1)).encode('utf-8')
    body1 = b'#' + numdigits1 + numbytes1 + binvalues1
    body1 = b'MAGIC 1000\n' + body1 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes2 = str(len(binvalues2)).encode('utf-8')
    numdigits2 = str(len(numbytes2)).encode('utf-8')
    body2 = b'#' + numdigits2 + numbytes2 + binvalues2
    body2 = b'MAGIC 1000\n' + body2 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    if save == True:
        f1 = open(fname1,'wb')
        f1.write(body1)
        f1.close()
        f2 = open(fname2,'wb')
        f2.write(body2)
        f2.close()
        return fname1,fname2
    return fname1,fname2
    
        
def generate_pulse_wfm(tstart=5, height1=0.9, height2=0.9, width1=10, width2=10, delay=150,
                       duration=256, clock=1e9, m1times=False, m2times=False ,save=True):
    '''Generates a waveform, saves it to E:/waveforms/, and returns the full filename
       tstart: time of first pulse in ns
       height 1,2 : ratio of pulse to max level for 1st and 2nd pulses
       width 1,2 : width of respective pulses in ns
       delay: time between pulses in ns
       duration: total duration of waveform file in ns
       clock: clock speed in samples per sec
       m1times (and m2times): list of times(ns) at which markers 1 and 2 should output a high signal
       save: boolean allowing the option to save; if False, returns the data block instead.
       -JF'''
    #from time import strftime
    #fname = "pulsewfm" + strftime("%Y%m%d-%H%M%S") + ".wfm"
    fname = unique_filename("E:/waveforms/","pulse","wfm")
    numpoints = int(duration * 1e-9 * clock + 0.5)
    if numpoints < 256 or numpoints > 4194048:
        print("There are too few or too many sample points in the waveform.")
        print("Please check clock and duration to ensure that 256 <= clock*duration <= 4194048")
        return ValueError
    values = np.zeros(numpoints,dtype='float32')
    markers = np.zeros(numpoints,dtype='int8')
    #timestep = float(numpoints/clock)
    width1steps = int(width1*1e-9*clock + 0.5)
    width2steps = int(width2*1e-9*clock + 0.5)
    delaysteps = int(delay*1e-9*clock + 0.5)
    start = int(tstart*1e-9*clock + 0.5)
    try:
        if m1times:
            m1index = [int(t*clock*1e-9) for t in m1times]
            for i in m1index:
                markers[i] += 1
        if m2times:
            m2index = [int(t*clock*1e-9) for t in m2times]
            for i in m2index:
                markers[i] += 2
    except IndexError:
        print('one or more markers are out of range for the duration')
    except:
        print('There was an error making the markers')
    if width1steps + width2steps + delaysteps + start >= numpoints:
        print("Duration is too short for given time parameters.")
        return ValueError
    if np.abs(height1) <= 1 and np.abs(height2) <= 1:
        values[start:start+width1steps] = height1
        values[start+width1steps+delaysteps:start+width1steps+width2steps+delaysteps] = height2
    else:
        print("height is out of range. Try again with a value between -1 and 1")
        return ValueError
    binvalues = b''
    for i,v in enumerate(values):
        binvalues += bytes(v) + struct.pack('<B',markers[i])
    numbytes = str(len(binvalues)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    body = b'#' + numdigits + numbytes + binvalues
    #trailer = b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    #packagedata = b'MAGIC 1000\n' + body + trailer
    body = b'MAGIC 1000\n' + body + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes = str(len(body)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    header = b'MMEM:DATA ' + b'"' + fname.encode('utf-8') + b'",#' + numdigits + numbytes
    #data = [bytes(v) + b'\x00' for v in values]
    if save == True:
        #filename = "E:/waveforms/" + fname
        #f = open(filename,'wb')
        f = open(fname,'wb')
        f.write(body)
        f.close()
        return fname
    else:
        return header + body

def convert2datablock(values,prefix,markers=False,clock=1e9,save=False):
    '''Converts an array of numpy float32 values to an AWG520 waveform.
       values: array (dtype='float32') of length between 256 and 4194048
       markers: array (dtype='int8') with same shape as values. defaults to constant low markers
       clock: waveform clock speed in samples per sec. defaults to 1e9'''
    # data validation. Should not be included if using generating many waveforms with good data.
    if len(values) < 256 or len(values) > 4194048:
        print('List of values is too short or too large. Should be between 256 and 4194048.')
        return False
    if not type(values[0]) == type(np.float32(0)):
        print('Wrong data type for values. Try again with numpy float32 data')
        return False
    if max(values) > 1 or min(values) < -1:
        print('Values out of range. Should be between -1 and 1.')
        return False
    if not markers:
        markers = np.zeros(len(values),dtype='int8')
    if not len(values) == len(markers):
        print("length of values and markers is not the same.")
        return False
    for m in markers:
        if not m in [0,1,2,3]:
            print('Markers are incompatible with AWG. Should contain only integers from 0 to 3')
            return False
    if not type(markers[0]) == type(np.int8(0)):
        print('Wrong data type for markers. Should be numpy int8.')
        return False
    
    # conversion code
    #from time import strftime
    #fname = "awg" + strftime("%Y%m%d-%H%M%S") + ".wfm"
    fname = unique_filename("E:/waveforms/",prefix,"wfm")
    file, path = os.path.split(fname)
    binvalues = b''
    for i,v in enumerate(values):
        binvalues += bytes(v) + struct.pack('<B',markers[i])
    numbytes = str(len(binvalues)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    body = b'#' + numdigits + numbytes + binvalues
    body = b'MAGIC 1000\n' + body + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes = str(len(body)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    header = b'MMEM:DATA ' + b'"' + file.encode('utf-8') + b'",#' + numdigits + numbytes
    if save == True:
        #filename = "E:/waveforms/" + fname
        #f = open(filename,'wb')
        f = open(fname,'wb')
        f.write(body)
        f.close()
    return header + body, fname

def convert2datablock_NV(fname,values,markers=False,clock=1e9,save=False):
    '''A shortened version of convert2datablock without data validation, to be used in quickly
       generating many waveform files. In this case, fname must be passed to the function from 
       the generator.
       -JF'''
    if not markers:
        markers = np.zeros(len(values),dtype='int8')
    binvalues = b''
    for i,v in enumerate(values):
        binvalues += bytes(v) + struct.pack('<B',markers[i])
    numbytes = str(len(binvalues)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    body = b'#' + numdigits + numbytes + binvalues
    body = b'MAGIC 1000\n' + body + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes = str(len(body)).encode('utf-8')
    numdigits = str(len(numbytes)).encode('utf-8')
    header = b'MMEM:DATA ' + b'"' + fname.encode('utf-8') + b'",#' + numdigits + numbytes
    if save == True:
        filename = "E:/waveforms/" + fname
        f = open(filename,'wb')
        f.write(body)
        f.close()
    return header + body, fname

def generate_gaussian(height,mean,stdev,duration,clock=1e9,markers=False):
    numpoints = int(duration * 1e-9 * clock + 0.5)
    data = np.zeros(numpoints, dtype="float32")
    times = np.linspace(0,duration,num=numpoints)
    for i, t in enumerate(times):
        data[i] = height*np.exp(-(t-mean)**2/(2*stdev**2))
    #print(type(values[0]))
    message,fname = convert2datablock(data,"gaussian",clock=clock)
    return message, fname
    
def generate_sinewave(height, frequency_Hz, numCycles, clock=1e9,markers=False,save=False):
    numpoints = int(numCycles/frequency_Hz * clock + 0.5)
    data = np.sin(np.arange(0,numpoints,dtype="float32")/clock * 2 * np.pi * frequency_Hz)
    message,fname = convert2datablock(data,"sine",markers=markers,clock=clock,save=save)
    return message, fname
    
def generateSpectroscopyPulses(tstart=25,height1=1, height2=1,width1=500,width2=500,duration=1200, clock=1e9, m1times=False, m2times=False ,save=True):
    fname1 = "E:/waveforms/Spectroscopy_Ch1_{}ns_{}ns.wfm".format(width1,width2)
    fname2 = "E:/waveforms/Spectroscopy_Ch2_{}ns_{}ns.wfm".format(width1,width2)
    numpoints = int(duration * 1e-9 * clock + 0.5)
    if numpoints < 256 or numpoints > 4194048:
        print("There are too few or too many sample points in the waveform.")
        print("Please check clock and duration to ensure that 256 <= clock*duration <= 4194048")
        return ValueError
    values1 = np.zeros(numpoints,dtype='float32')
    values2 = np.zeros(numpoints,dtype='float32')
    markers1 = np.zeros(numpoints,dtype='int8')
    markers2 = np.zeros(numpoints,dtype='int8')
    width1steps = int(width1*1e-9*clock + 0.5)
    width2steps = int(width2*1e-9*clock + 0.5)
    start = int(tstart*1e-9*clock + 0.5)
    markers2[start+width1steps:start+width1steps+100] += 3 #extra indices to eliminate the pre-trigger capture by Alazar
    if width1steps + width2steps + start >= numpoints:
        print("Duration is too short for given time parameters.")
        return ValueError
    if np.abs(height1) <= 1 and np.abs(height2) <= 1:
        values1[start:start+width1steps] = height1
        values2[start+width1steps:start+width1steps+width2steps] = height2
    else:
        print("height is out of range. Try again with a value between -1 and 1")
        return ValueError
    binvalues1 = b''
    binvalues2 = b''
    for i,v in enumerate(values1):
        binvalues1 += bytes(v) + struct.pack('<B',markers1[i])
    for i,v in enumerate(values2):
        binvalues2 += bytes(v) + struct.pack('<B',markers2[i])
    numbytes1 = str(len(binvalues1)).encode('utf-8')
    numdigits1 = str(len(numbytes1)).encode('utf-8')
    body1 = b'#' + numdigits1 + numbytes1 + binvalues1
    body1 = b'MAGIC 1000\n' + body1 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    numbytes2 = str(len(binvalues2)).encode('utf-8')
    numdigits2 = str(len(numbytes2)).encode('utf-8')
    body2 = b'#' + numdigits2 + numbytes2 + binvalues2
    body2 = b'MAGIC 1000\n' + body2 + b'CLOCK ' + ("%10e\r\n" % clock).encode('utf-8')
    if save == True:
        f1 = open(fname1,'wb')
        f1.write(body1)
        f1.close()
        f2 = open(fname2,'wb')
        f2.write(body2)
        f2.close()
        return fname1,fname2
    return fname1,fname2
