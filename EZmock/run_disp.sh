#!/bin/bash

redshift=2
fnl=600
Lbox=2000
Ngrid=512

mkdir -p /pscratch/sd/s/siyizhao/2LPTdisp/
cd /global/u1/s/siyizhao/projects/learnCosm/EZmock
srun -N1 -C gpu -t 04:00:00 --qos interactive --account desi -n1 python scripts/run_disp.py --redshift $redshift --fnl $fnl --Lbox $Lbox --Ngrid $Ngrid 

cd /pscratch/sd/s/siyizhao/2LPTdisp/
mv dispx_42.txt dx_42_z${redshift}L${Lbox}N${Ngrid}fnl${fnl}.txt
mv dispy_42.txt dy_42_z${redshift}L${Lbox}N${Ngrid}fnl${fnl}.txt
mv dispz_42.txt dz_42_z${redshift}L${Lbox}N${Ngrid}fnl${fnl}.txt
# then fit or calibrate EZmocks using the displacement files generated
