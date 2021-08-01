import json
import numpy as np
from matplotlib import pyplot as plt
import math


def get_N_RA_DEC():
    with open("joined_timekey_folder/L1.json", "r") as f:
        times = json.load(f)
    
    N=int(math.sqrt(len(times)*2))
    N_RA=N
    N_DEC=math.floor(N/2)
    
    return N, N_RA, N_DEC
    
    
def get_times(DET):
    with open("joined_timekey_folder/{}.json".format(DET), "r") as f:
        times = json.load(f)
    
    N=int(math.sqrt(len(times)*2))
    N_RA=N
    N_DEC=math.floor(N/2)
    array_times=np.full((N_DEC,N_RA),0.0)

    for key in times.keys():
        co_ords=list(key.split('_'))
        RA_j=int(co_ords[0])
        DEC_i=int(co_ords[1])
    
        array_times[DEC_i][RA_j]=times[key]

    return array_times


def heat_plotter(array, N_RA, N_DEC, name):
    RA=[str(2*np.pi*(i/8))[:4] for i in range(8)]
    RA_i=[N_RA*i/8 for i in range(8)]
    DEC=[str(np.pi*(j/8))[:4] for j in range(8)]
    DEC_j=[ N_DEC*j/8 for j in range(8)]

    harvest = array

    plt.imshow(harvest, origin='lower')

    plt.xlabel('ra',fontsize=15)
    plt.xticks(RA_i, RA)
    plt.xticks(fontsize=10)

    plt.ylabel('dec', fontsize=15)
    plt.yticks(DEC_j,DEC)
    plt.yticks(fontsize=10)

    plt.title(name, fontsize=20)
    plt.tight_layout()

    cbar=plt.colorbar();
    cbar.ax.tick_params(labelsize=10) 

    plt.savefig("plots/{}.png".format(name))
    plt.close()
    
def histo_plotter(array1, array2, array3):
    lab1='L1/V1'+" "+str(max(array1.flatten()))[:7]
    lab2='L1/H1'+" "+str(max(array2.flatten()))[:7]
    lab3='V1/H1'+" "+str(max(array3.flatten()))[:7]
    
    
    plt.hist(array1.flatten(), alpha=0.5, label=lab1)
    plt.hist(array2.flatten(), alpha=0.5, label=lab2)
    plt.hist(array3.flatten(), alpha=0.5, label=lab2)
    plt.legend(loc='upper right')
    plt.savefig("plots/{}.png".format("differences"))
    plt.close()
    
if __name__=="__main__":
    N, N_RA, N_DEC = get_N_RA_DEC()

    L1=get_times("L1")
    V1=get_times("V1")
    H1=get_times("H1")

    L1_V1=np.abs(L1-V1)
    L1_H1=np.abs(L1-H1)
    V1_H1=np.abs(V1-H1)

    heat_plotter(L1, N_RA, N_DEC, 'L1')
    heat_plotter(V1, N_RA, N_DEC, 'V1')
    heat_plotter(H1, N_RA, N_DEC, 'H1')

    heat_plotter(L1_V1, N_RA, N_DEC, 'L1_V1')
    heat_plotter(L1_H1, N_RA, N_DEC, 'L1_H1')
    heat_plotter(V1_H1, N_RA, N_DEC, 'V1_H1')
    
    histo_plotter(L1_V1, L1_H1, V1_H1)
    