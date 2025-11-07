# Usage: run `bash run_disp.sh ;exit` on an interactive allocation (salloc -A desi -C cpu -q interactive -t 04:00:00 -N 1)

srun -N1 -n1 python scripts/run_disp.py 

rm -f rand_ampl.bin
rm -f rand_phase.bin

# then fit or calibrate EZmocks using the displacement files generated
