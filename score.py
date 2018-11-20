#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 09:29:38 2016

@author: blau
uses mne_find_events to extract stimulus onsets (1 trigger)
events defined manually below - 100 trials pitch, 100 trials speech

# final scoring function for pitch_acc
"""

# -*- coding: utf-8 -*-

import numpy as np
import warnings
import mne
from mnefun._paths import get_raw_fnames, get_event_fnames


def score(p, subjects, run_indices):
    """Default scoring function that just passes event numbers through"""
    for si, subj in enumerate(subjects):
        print('  Scoring subject %s... ' % subj)

        raw_fnames = get_raw_fnames(p, subj, 'raw', False, False,
                                    run_indices[si])
        eve_fnames = get_event_fnames(p, subj, run_indices[si])

        for raw_fname, eve_fname in zip(raw_fnames, eve_fnames):
            with warnings.catch_warnings(record=True):
                raw = mne.io.read_raw_fif(raw_fname, allow_maxshield='yes')
            events_raw = mne.find_events(raw, stim_channel='STI101',
                                         shortest_event=0)
            # where event trigs = 1
            start_inds = np.where(events_raw[:, -1] == 1)[0]
            # generate empty matrix with len events, 3 for event type
            event_type = np.zeros((len(start_inds), 3))
            # take all samples marked with 1 trigger (stim onset)
            events = events_raw[start_inds, :]
            assert len(events) == 200  # otherwise something is wrong
            # :100 - pitch 100: - speech 100 trials for full data set
            event_type[:100, -1] = 10  # 'pitch'
            event_type[100:, -1] = 20  # 'speech'
            events[:, -1] = event_type[:, -1]
            mne.write_events(eve_fname, events)
