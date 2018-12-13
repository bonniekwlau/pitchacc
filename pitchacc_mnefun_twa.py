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

params = mnefun.Params(tmin=-0.2, tmax=2, n_jobs=8,
                       decim=2, proj_sfreq=200, n_jobs_fir='cuda',
                       filter_length='auto', lp_cut=80.,
                       n_jobs_resample='cuda', cov_method='shrunk',
                       bmin=-0.1, bem_type='5120')
params.subjects_dir = 'subjects'
params.subjects = ['pitchacc_108']
params.structurals = params.subjects
params.dates = [None] * len(params.subjects)  # None used to fully anonymize
params.score = score  # scoring function used to slice data into trials
# define which subjects to run
params.subject_indices = np.arange(len(params.subjects))
params.plot_drop_logs = True

# Set parameters for remotely connecting to acquisition computer
params.acq_ssh = 'bonnie@172.28.161.8'  # minea
# params.acq_ssh = 'bonnie@sinuhe.ilabs.uw.edu'  # minea
params.acq_dir = '/sinuhe/data01/pitchacc'

# Set parameters for remotely connecting to SSS workstation ('sws')
# params.sws_ssh = 'bonnie@172.25.148.15' #use sinuhe for MF 2.1
params.sws_ssh = 'localhost'  # 'bonnie@kasga.ilabs.uw.edu'  # use sinuhe for MF 2.1
params.sws_port = 2222
params.sws_dir = '/mnt/bakraid/data/sss_work'  # '/home/bonnie/'

#  SSS Options
# python | maxfilter for choosing SSS applied using either Maxfilter or MNE
params.sss_type = 'python'
params.sss_regularize = 'in'
params.tsss_dur = 4.
params.int_order = 6
params.st_correlation = .95
params.trans_to = 'twa'  # (0,0,0.3)  # (0,0,0.04) or 'median'
params.movecomp = 'inter'
params.coil_dist_limit = 0.01  # be mroe tolerant
# Trial/CH rejection criteria
params.reject = dict(grad=3000e-13, mag=4000e-15)
params.flat = dict(grad=1e-13, mag=1e-15)
params.ssp_ecg_reject = dict(grad=3000e-13, mag=6000e-15)
params.run_names = ['%s_01']
params.get_projs_from = np.arange(1)
params.inv_names = ['%s']
params.inv_runs = [np.arange(1)]
params.runs_empty = ['%s_erm']
# Define number of SSP projectors. Columns correspond to Grad/Mag/EEG chans
params.proj_nums = [[1, 1, 0],  # ECG: grad/mag/eeg
                    [0, 0, 0],  # EOG
                    [0, 0, 0]]  # Continuous (from ERM)
params.proj_ave = True
params.compute_rank = True
params.cov_rank = None

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

times = [0.25, 0.5]
params.report_params.update(
    bem=False,
    whitening=dict(analysis='All', name='All', cov='%s-80-sss-cov.fif'),
    ssp_topomaps=True,
    sensor=[
        dict(analysis='Conditions', name='pitch', times=times),
        dict(analysis='Conditions', name='speech', times=times),
        ],
    source_alignment=True,
    source=[
        dict(analysis='Conditions', name='pitch', times=times,
             inv='%s-80-sss-meg-free-inv.fif', views=['lat', 'med'],
             size=(800, 800)),
        dict(analysis='Conditions', name='speech', times=times,
             inv='%s-80-sss-meg-free-inv.fif', views=['lat', 'med'],
             size=(800, 800)),
        ],
    psd=False,
    )
default = False
mnefun.do_processing(
    params,
    fetch_raw=default,
    do_score=default,
    push_raw=default,
    do_sss=default,
    fetch_sss=default,
    do_ch_fix=default,
    gen_ssp=default,
    apply_ssp=default,
    write_epochs=default,
    gen_covs=default,
    gen_fwd=default,
    gen_inv=default,
    gen_report=True,
    print_status=False,
)
