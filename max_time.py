import sys;
import os;
import numpy as np;
import pylab as pl;

import pycbc.waveform;
from pycbc.detector import Detector;
import argparse;
import json;

    
def get_gw_coa_times( DET, RA, DEC, N):
    
    #build parameters
    mass1, mass2 = 50, 50
    spin1x, spin1y, spin1z = 0.0, 0.0, 0.0
    spin2x, spin2y, spin2z = 0.0, 0.0, 0.0
    distance = 0.1 # Close distance so that the injection can be seen in the data
    inclination = 0.1
    polarization = 0.3
    lambda1, lambda2 = 0.0, 0.0
    coa_phase = 1.1
    f_lower = 15
    f_ref = 0
    approximant = 'IMRPhenomPv2_NRTidalv2'
    t = 1264069376
    
    #input RA/DEC:
    RA_N=N
    DEC_N=N/2
    ra, dec = 2*np.pi*(RA/RA_N), np.pi*(DEC/DEC_N)
    print(DET,": ",str((RA/RA_N))," ",str((DEC/DEC_N)))
    
    print("making waveform..")
    #create a GW waveform
    hp, hc = pycbc.waveform.get_td_waveform(approximant='IMRPhenomPv2_NRTidalv2', mass1=mass1,
                                        mass2=mass2, lambda1=lambda1, lambda2=lambda2,
                                        spin1x=spin1x, spin1y=spin1y, spin1z=spin1z,
                                        spin2x=spin2x, spin2y=spin2y, spin2z=spin2z,
                                        distance=distance, inclination=inclination,
                                        coa_phase=coa_phase, f_lower=f_lower, f_ref=f_ref,
                                        polarization=polarization, delta_t=1/16384);
    
    print("projecting waveform...")
    #Project the wave into a detector
    d = Detector(DET);
    hp.start_time = hc.start_time = t - hp.duration;
    h = d.project_wave(hp, hc, ra, dec, polarization);
    
    print("getting max t0")
    #get projected data
    time_series=h.sample_times.data
    function_height=h.data
    
    #get coalescence time
    MAX_F_INDX=function_height.argmax()
    coa_time=time_series[MAX_F_INDX]
    
    print("dumping...")
    # MAX_OS holds trialn's max onsource peak
    key_ra_dec=str(RA)+"_"+str(DEC)
    COA_DIC={key_ra_dec : coa_time }
    with open("indiv_timekey_folder/{}_keys/{}_{}_{}.json".format(DET,DET,str(ra),str(dec)), "w") as f:
        json.dump(COA_DIC, f, indent=2, sort_keys=True)

    print("done!")

if __name__=="__main__":

    sys.stdout = open(os.devnull, 'w')
    print("entering parser...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--det', type=str)
    parser.add_argument('--ra', type=int)
    parser.add_argument('--dec', type=int)
    parser.add_argument('--N', type=int)

    args = parser.parse_args()

    print("entering gw_coa_times")
    get_gw_coa_times(args.det, args.ra, args.dec, args.N)    #write strings input with quotes
    
    #enables print
    sys.stdout = sys.__stdout__
    print("done!")
    
