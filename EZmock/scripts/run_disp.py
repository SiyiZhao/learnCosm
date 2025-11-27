import argparse
import sys, os
current_dir = os.getcwd()
source_dir = os.path.join(current_dir, "src")
if source_dir not in sys.path:
    sys.path.insert(0, source_dir)
from disp2LPT_helper import run_disp_2lpt

def parse_args():
    parser = argparse.ArgumentParser(description="Run 2LPT displacement field generation")
    parser.add_argument('--seed', type=int, default=42, help='Random seed for initial conditions')
    parser.add_argument('--redshift', type=float, default=2.0, help='Redshift at which to compute displacements')
    parser.add_argument('--fnl', type=float, default=600, help='Non-Gaussianity parameter f_NL')
    parser.add_argument('--Lbox', type=int, default=2000, help='Box size in Mpc/h')
    parser.add_argument('--Ngrid', type=int, default=512, help='Grid size for the simulation')
    return parser.parse_args()
args = parse_args()
seed = args.seed
redshift = args.redshift
fnl = args.fnl
Lbox = args.Lbox
Ngrid = args.Ngrid

run_disp_2lpt(seed=seed, redshift=redshift, fnl=fnl, Ngrid=Ngrid, Lbox=Lbox, fix_amp=1) # fixed amplitude for calibration of EZmock
