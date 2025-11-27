#!/bin/bash

cd 2LPTdisp
mv dispx_42.txt dx_42_z3L1000N256fnl400.txt
mv dispy_42.txt dy_42_z3L1000N256fnl400.txt
mv dispz_42.txt dz_42_z3L1000N256fnl400.txt

cd ..
# modeified fnl in the script
python genEZmock-z3.py 

source /global/common/software/desi/users/adematti/cosmodesi_environment.sh main
# add the new case in the script
python plot-ezmock-z3.py 
