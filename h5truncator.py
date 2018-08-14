#!/usr/bin/python

#Open and truncate copied hdf5 file for handling with MEA tools, won't go longer than 23 mins for some reason

import h5py as h5
import numpy as np

f = h5.File('truncatedWTRepeat.h5', 'r+')

group = f['Data']
rec = group['Recording_0']
aStream = rec['AnalogStream']
stream0 = aStream['Stream_0']
chandata = stream0['ChannelData']
trunc_chan = chandata[:, 6000000:]
del stream0['ChannelData']
stream0['ChannelData'] = trunc_chan




