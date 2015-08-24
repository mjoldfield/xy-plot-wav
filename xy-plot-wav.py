#
# xy-plot-wav.py
#
# See:
#    https://github.com/mjoldfield/xy-plot-wav
#    http://www.mjoldfield.com/atelier/2015/08/xy-sound.html
#
# All the good things in here are ripped off from:
#    http://wiki.scipy.org/Cookbook/EyeDiagram
#    http://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
#
# Bugs:
#   - the WAV file must be in 16-bit signed-integer PCM format
#
# To grab a suitable file in SoX:
#    $ sox -d  -e signed-integer -b 16 foo.wav trim 0 5
# 

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf

import sys
import argparse

def plot_wav_file(filename):

    print "Reading " + filename
    (rate, data) = wf.read(filename)

    (samples, channels) = data.shape
    if channels == 2:
        print "   %d samples at %.1fkHz" % (samples, rate / 1000.0)
        plot_wav_data(data)
    else:
        print "   invalid format: need 2 channels but got %d" % channels


def plot_wav_data(data, grid_size=512):
    
    wav_range = 65536

    grid = np.zeros((grid_size, grid_size), dtype=np.int32)

    # rescale to grid coords
    coords =  (data + (wav_range / 2)) / (wav_range / grid_size)

    # tally counts
    for [x,y] in coords:
        grid[x,y] += 1
        
    # convert to floats, use NaN for unseen pixels, and squash range with log
    grid = grid.astype(np.float32)
    grid[grid==0] = np.nan
    grid = np.log(grid)
        
    # plot it
    plt.figure()
    plt.grid(color='w')
    plt.imshow(grid.T[::-1,:], extent=[0,1,0,1], cmap=plt.cm.summer)
    
    ax = plt.gca()
    ax.set_axis_bgcolor('k')
    ax.set_xticks(np.linspace(0,1,11))
    ax.set_yticks(np.linspace(0,1,11))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
if __name__ == '__main__':
     p = argparse.ArgumentParser(description='Plot XY data from WAV files')
     p.add_argument(dest='filenames', metavar='filename', nargs='*')
     
     args = p.parse_args()     

     for filename in args.filenames:
         plot_wav_file(filename)
         
     plt.show()
         
