# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:45:47 2016

@author: mdclarke
"""

import mne

subjs = ['pitchacc_otso_01']
      
int_order = 6
ext_order = 3
st_dur = 6.
st_correlation = 0.90
tmin, tmax = -0.2, 2.
destination =(0,0,0.03)
reg = 'svd'
cal_file = '/Users/blau/Desktop/MegData/sss_cal.dat'
cross_file = '/Users/blau/Desktop/MegData/ct_sparse.fif'
         
for i in subjs:
    data_path = ('/Users/blau/Desktop/MegData/')
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
    event_id = {'onset' :1}
    epochs = mne.Epochs(maxfilt, events, event_id, tmin=tmin, tmax=tmax,
                        reject=None, baseline=None, proj=False)
    del maxfilt                    
    evoked = epochs.average()
    evoked.plot()
    #evoked.plot(spatial_colors=True)

    #evoked.save(data_path + '%s_raw_mc_svd_tsss_90_noBL-ave.fif' %i)
