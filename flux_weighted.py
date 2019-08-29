#! /usr/bin/env python

import numpy as np
import os
import glob
from scipy import integrate
from astropy.table import Table
from astropy.io import ascii
import matplotlib.pyplot as pl

lsf_dir = "/user/jotaylor/COS/LSFs"
lsfs = glob.glob(os.path.join(lsf_dir, "aa_LSFTable*.dat"))
weight = 1

for item in lsfs:
    fig = pl.figure(figsize=(15,10))
    ax = fig.add_subplot(111)
    data = Table.read(item, format="ascii.basic")
    centroids = []
    for column in data.columns:
        y = data[column]
#        x = np.arange(len(data[column]))
        N = len(y)
        x0 = np.arange(-(N-1)/2., (N+1)/2.,1)
        x = x0.astype(np.float64)
        centroid = integrate.simps(weight*x*y, x) / integrate.simps(weight*y, x)
#        centroid = np.sum(x*y) / np.sum(x)
        centroids.append(centroid)
   
    maxdiff = max(centroids) - min(centroids)
    ax.plot(data.keys(), centroids, marker=".")
    
    sp = item.split("_")
    grating = sp[2]
    if "LP1" in item:
        lp = sp[3]
        figname = "{0}_{1}_centroid2.png".format(grating, lp)
        titlename = "{0} {1} LSF Centroids, Max Diff={2:3.2f} pix".format(grating, lp, maxdiff)
    else:
        cenwave = sp[3]
        lp = sp[4]
        figname = "{0}_{1}_{2}_centroid2.png".format(grating, cenwave, lp)
        titlename = "{0}/{1} {2} LSF Centroids, Max Diff={3:3.2f} pix".format(grating, cenwave, lp, maxdiff)
    
    ax.set_title(titlename)
    ax.set_xlabel("Wavelength Bin")
    ax.set_ylabel("Relative Pixel")
    fig.savefig(figname)
    print("Saved {0}".format(figname))
