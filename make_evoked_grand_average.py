#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:10:21 2019

Read in evoked files (must be in same head position), and make grand average 
for group level analysis

Good only = dropped 123, 125, 126, 128, 142, 152 (n=)

@author: blau
"""

import os.path as op
import mne
import numpy as np
#from mne.viz import plot_arrowmap

print(__doc__)

data_dir = '/home/blau/pitchacc/hp30/6M/'
subjects = ['pitchacc_152v2', 'pitchacc_109v2']
condition = ['pitch', 'speech']

evokeds_list = []
naves = np.zeros(len(subjects), int)
for ni, si in enumerate(subjects):
    fname = op.join(data_dir, '%s' %si, 'inverse', 'Conditions_80-sss_eq_%s-ave.fif' %si)
    evokeds = mne.read_evokeds(fname, condition=condition, baseline=(None,0), proj=True)
    nave = np.unique([a.nave for a in evokeds])
    naves[ni] = nave
    evokeds_list += [evokeds]
all_evokeds = np.concatenate(evokeds_list)
grand_average = mne.grand_average(all_evokeds)
#mne.write_evokeds('pitchacc_hp30_6M_grand-ave.fif', grand_average)


