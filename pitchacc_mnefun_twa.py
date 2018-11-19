# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:45:31 2017

mnefun script for pitchacc
final 10/26/17
AIM 1 - headpos (0,0,0.03) to match previous analysis
AIM 2 - headpos median for more accurate sequential dipole fitting

data set notes:
pitchacc_01 and pitchacc_04 only have pitch conditions trials
    adjust epoching params and score function
pitchacc_07_01 has 100 pitch trials and a few unusable speech trials
pitchacc_07_02 has 52 speech trials - not sure if they are usable


@author: blau
"""

import mnefun
import numpy as np
from score import score

try:
    # Use niprov as handler for events if it's installed
    from niprov.mnefunsupport import handler
except ImportError:
    handler = None

params = mnefun.Params(tmin=-0.2, tmax=2, n_jobs=8,
                       decim=2, proj_sfreq=200, n_jobs_fir='cuda',
                       filter_length='5s', lp_cut=80., n_jobs_resample='cuda',
                       bmin=-0.1)
params.subjects = ['pitchacc_108_01']
# added -force -autobad off to line 956 in mnefun.py
# removed 'copy=False' from line 1391, in save_epochs
# changed mnefun.py line 1048 to 'bad_condition='warning' to bypass bad
# matrix error
params.structurals = [None] * len(params.subjects)  # None means use sphere
params.dates = [None] * len(params.subjects)  # None used to fully anonymize
params.score = score  # scoring function used to slice data into trials
# define which subjects to run
params.subject_indices = np.arange(len(params.subjects))
params.plot_drop_logs = False  # Turn off so plots do not halt processing

# Set parameters for remotely connecting to acquisition computer
params.acq_ssh = 'bonnie@172.28.161.8'  # minea
# params.acq_ssh = 'bonnie@sinuhe.ilabs.uw.edu'  # minea
params.acq_dir = '/sinuhe/data03/pitchacc'

# Set parameters for remotely connecting to SSS workstation ('sws')
# params.sws_ssh = 'bonnie@172.25.148.15' #use sinuhe for MF 2.1
params.sws_ssh = 'bonnie@kasga.ilabs.uw.edu'  # use sinuhe for MF 2.1
params.sws_dir = '/home/bonnie/'

#  SSS Options
# python | maxfilter for choosing SSS applied using either Maxfilter or MNE
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4.
params.int_order = 6
params.st_correlation = .95
params.trans_to = 'twa'  # (0,0,0.3)  # (0,0,0.04) or 'median'
params.movecomp = 'inter'
params.coil_bad_count_duration_limit = 0.1
# Trial/CH rejection criteria
# params.reject = dict(grad=3000e-13, mag=4000e-15)
params.reject = dict()
params.flat = dict(grad=1e-13, mag=1e-15)
# params.auto_bad_reject = dict(grad=3000e-13, mag=4000e-15)
params.auto_bad_reject = None
params.ssp_ecg_reject = dict(grad=3000e-13, mag=6000e-15)
# params.ssp_ecg_reject  = None
params.auto_bad_flat = None
params.auto_bad_meg_thresh = 10
params.run_names = ['%s']
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.runs_empty = []
# Define number of SSP projectors. Columns correspond to Grad/Mag/EEG chans
params.proj_nums = [[0, 0, 0],  # ECG: grad/mag/eeg
                    [0, 0, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)

params.cov_method = 'empirical'  # Cleaner noise covariance regularization
params.compute_rank = True
# params.bem_type = '5120'
# params.plot_head_position = True  # Plot cHPI data for single raw file
# By default SSP projection scalp topography maps will be saved in
# sss_pca_folder for inspection. To avoid having images saved to disk set
# params.plot_pca = False
# params.plot_drop_logs = True

# Epoching: scoring function needs to produce an event file with these values
params.in_numbers = [10, 20]
# Those values correspond to real categories as:
params.in_names = ['pitch', 'speech']
# Define how to translate the above event types into evoked files
params.analyses = ['All',
                   'Conditions']
params.out_names = [['All'],
                    ['pitch', 'speech']]
params.out_numbers = [[1, 1],  # Combine all trials
                      [1, 2]]
params.must_match = [
    [],
    [0, 1],  # Only ensure the standard event counts match
]

pitch_times = [0.1, 0.2]
speech_times = [0.1, 0.2]
params.report_params.update(
    bem=False,
    whitening=False,
    ssp_topomaps=True,
    sensor=[
        dict(analysis='Conditions', name='pitch', times=pitch_times),
        dict(analysis='Conditions', name='speech', times=speech_times)],
    source_alignment=False,
    source=False,
    psd=False,
    )
mnefun.do_processing(
    params,
    fetch_raw=False,
    push_raw=False,
    do_sss=False,
    fetch_sss=False,
    do_score=False,
    do_ch_fix=False,
    gen_ssp=False,
    apply_ssp=False,
    write_epochs=False,
    gen_covs=False,
    gen_fwd=False,
    gen_inv=False,
    gen_report=True
    ,
    print_status=False,
)
