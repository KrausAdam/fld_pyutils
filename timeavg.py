import os.path
import sys
import numpy as np

#ENTER STUFF HERE
sys.path.append('/lustre/orion/nfu106/scratch/arkraus/fld_pyutils/') # repo path
fpath = '/lustre/orion/nfu106/scratch/arkraus/budgetTest/NEWKasagi_Plugin/run11/' # averaging path
outpath = fpath # output path
fname = 'ra2kasagi' # assumes 'fname0.f*' file format
fstart = 1 # file index to start the averaging (sequential)
outpref = 'TAVG' # output named 'outpreffname0.f00001'

#DON'T TOUCH

from fld_data_memmap import FldDataMemmap
from fld_data import FldData

fnum = '0000' + str(fstart)
totname = fpath + fname + '0.f' + fnum[-5:]

avg = FldDataMemmap.fromfile(totname, mode='c')
# avg = FldData.fromfile(totname)

avg.u = np.full((avg.nelt, avg.ndims, avg.nx1 * avg.ny1 * avg.nz1), fill_value=0.0)
avg.p = np.full((avg.nelt, avg.nx1 * avg.ny1 * avg.nz1), fill_value=0.0)
avg.t = np.full((avg.nelt, avg.nx1 * avg.ny1 * avg.nz1), fill_value=0.0)
if avg.nscalars:
    avg.s = np.full((avg.nscalars, avg.nelt, avg.nx1 * avg.ny1 * avg.nz1), fill_value=0.0)

#time weighting
atime = 0.0
dtime = 0.0

beta = 1.0
alpha = 1.0 - beta

#time averaging
while os.path.isfile(totname):
    f = FldDataMemmap.fromfile(totname)
    # f = FldData.fromfile(totname)
    dtime = f.time
    atime = atime + dtime
    beta = dtime/atime
    alpha = 1.0 - beta
    avg.u = alpha*avg.u + beta*f.u
    avg.p = alpha*avg.p + beta*f.p
    avg.t = alpha*avg.t + beta*f.t
    if avg.nscalars:
        avg.s = alpha*avg.s + beta*f.s
    fstart = fstart + 1
    fnum = '0000' + str(fstart)
    totname = fpath + fname + '0.f' + fnum[-5:]

# output time will be the summed averaging time
avg.time = atime

avg.tofile(outpath+outpref+fname+'0.f00001')

