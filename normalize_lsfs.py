#! /usr/bin/env python

import os
import glob
from scipy import integrate
from astropy.table import Table
from astropy.io import ascii

#lsf_dir = "/user/jotaylor/COS/LSFs/LP4"
#lsf_dir = "/grp/hst/cos/cos_lsfs"
lsf_dir = "/grp/hst/cos3/jo_codeV/G130M_Data/Data_1Ang_LP1/PSFData_G130M_1291"
lsfs = glob.glob(os.path.join(lsf_dir, "*.dat"))

for item in lsfs:
    lsfname = os.path.basename(item)
    if "LP1" in lsfname:
        continue
    
    if "LP" not in lsfname:
        tablename = lsfname.split(".dat")[0] + "_LP4_norm.dat"
    else:
        tablename = lsfname.split(".dat")[0] + "_normjo.dat"

    data = Table.read(item, format="ascii.basic")
    newcols = []
    for column in data.colnames:
        total = integrate.simps(data[column])
        newcols.append(data[column] / total)

    t = Table(newcols, names=data.colnames)
    t.write(tablename, format="ascii.basic")
    print("Wrote {0}".format(tablename))

