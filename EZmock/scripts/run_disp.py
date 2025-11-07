import sys, os
current_dir = os.getcwd()
source_dir = os.path.join(current_dir, "src")
if source_dir not in sys.path:
    sys.path.insert(0, source_dir)
from disp2LPT_helper import run_disp_2lpt

seed = 43
redshift = 0.95
fnl=1200
# Lbox = 1000
# Ngrid = 256
Lbox = 2000
Ngrid = 512

run_disp_2lpt(seed=seed, redshift=redshift, fnl=fnl, Ngrid=Ngrid, Lbox=Lbox, fix_amp=1) # fixed amplitude for calibration of EZmock
