# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:45:47 2016

Added breakdown of conditions for subjects with data from both "pitch" and "speech". 

@author: mdclarke
"""

import mne
import numpy as np

subjs = ['pitchacc_109_01']
      
int_order = 6
ext_order = 3
st_dur = 6.
st_correlation = 0.90
tmin, tmax = -0.2, 2.
destination =(0,0,0.03)
reg = 'svd' # changed from svd
cal_file = '/Users/blau/pitchacc/original/sss_cal.dat'
cross_file = '/Users/blau/pitchacc/original/ct_sparse.fif'
         
for i in subjs:
    data_path = ('/Users/blau/pitchacc/original/')
    fname = (data_path + '%s_raw.fif' %i)
    raw = mne.io.Raw(fname, allow_maxshield='yes', preload=True)
    tsss_fname = (data_path + '%s_raw_mc_svd_tsss_90_noBL.fif' %i)
    pos = mne.chpi.read_head_pos(data_path + '%s_raw.pos' %i)
    # fix magnetometer coil types
    raw.fix_mag_coil_types()
    # remove cHPI signals
    mne.chpi.filter_chpi(raw, verbose=True)
    # apply maxwell filter
    maxfilt = mne.preprocessing.maxwell_filter(raw, int_order=int_order, 
                                               ext_order=ext_order,
                                               calibration=cal_file,
                                               cross_talk=cross_file,
                                               st_correlation=st_correlation, 
                                               st_duration=st_dur,
                                               head_pos=pos, 
                                               destination=destination, 
                                               regularize=reg,
                                               bad_condition='ignore', 
                                               verbose=True)
    del raw                                               
    maxfilt.save(tsss_fname, overwrite=True)
    events = mne.find_events(maxfilt, stim_channel='STI101')
    # where event trigs = 1
    start_inds = np.where(events[:, -1] == 1)[0]
    # generate empty matrix with len events, 3 for event type
    event_type = np.zeros((len(start_inds), 3))
    # take all samples marked with 1 trigger (stim onset)
    events = events[start_inds, :]
    # :100 - pitch 100: - speech 100 trials for full data set
    event_type[:100, -1] = 10  # 'pitch'
    event_type[100:, -1] = 20  # 'speech'
#            event_type[:,-1] = 10 #'pitch'
    events[:, -1] = event_type[:, -1]    
    event_id = {'pitch' :10, 'speech' : 20}
    epochs = mne.Epochs(maxfilt, events, event_id, tmin=tmin, tmax=tmax,
                        reject=None, baseline=None, proj=False)
    del maxfilt                    
    evoked = epochs.average()
    evoked.plot(spatial_colors=True)
    evoked.save(data_path + '%s_raw_mc_svd_tsss_90_noBL-ave.fif' %i)
