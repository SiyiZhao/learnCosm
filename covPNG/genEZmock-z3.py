# %%
import os
import numpy as np
from EZmock import EZmock

# %% [markdown]
# ## Read Reference Mock

# %%
fnl =1200
redshift = 3.0

# %%
num = 4985722

# %% [markdown]
# ## EZmock Setup

# %%
# EZmock parameters
Omega_m0 = 0.3137721
Omega_nu = 0.00141976532
ncpu = 64
# Factor to be multiplied to the z-velocities for redshift-space distortion
rsd_fac = (1 + redshift) / (100 * np.sqrt(Omega_m0 * (1 + redshift)**3 + (1 - Omega_m0)))
# Output directory, should be large enough, we recommend to make a soft link to $SCRATCH
odir = 'out'

# %%
def setup_ez(Lbox=1000, Ngrid=256, seed=42):
    # Initialize EZmock instance
    ez = EZmock(Lbox=Lbox, Ngrid=Ngrid, seed=42, nthread=ncpu)
    ez.eval_growth_params(z_out=redshift, z_pk=1, Omega_m=Omega_m0, Omega_nu=Omega_nu)

    mydx=np.loadtxt(f'/pscratch/sd/s/siyizhao/2LPTdisp/dx_{seed}.txt')
    mydy=np.loadtxt(f'/pscratch/sd/s/siyizhao/2LPTdisp/dy_{seed}.txt')
    mydz=np.loadtxt(f'/pscratch/sd/s/siyizhao/2LPTdisp/dz_{seed}.txt')
    ez.create_dens_field_from_disp(mydx,mydy,mydz, deepcopy=True)
    return ez

# %%
# Lbox = 2000
# Ngrid = 512
# seed = 43
# ntracer = num
## to speed up the process during calibration, you can use smaller box and lower grid resolution first, and then go back to the right setting for final check
Lbox = 1000
Ngrid = 256
seed = '42_z3L1000N256fnl1200'  # seed can be a string
ntracer = num//8

ez = setup_ez(Lbox=Lbox, Ngrid=Ngrid, seed=seed)


# %% [markdown]
# ### run and plot EZmock

# %%
def run_and_plot_EZmock(ez, pyc, params):
    """
    Run EZmock with the given parameters and plot the clustering statistics.
    
    Parameters:
    ez (EZmock): The EZmock instance.
    pyc (pyclustering): The pyclustering instance.
    params (dict): List of EZmock parameters to be run.
    """
    fnames = []
    for param in params:
        rho_c, rho_exp, pdf_base, sigma_v = param
        fname = f'{odir}/EZmock_L{Lbox:g}_N{Ngrid:d}_fnl{fnl:g}_c{rho_c:g}_e{rho_exp:g}_b{pdf_base:g}_v{sigma_v:g}.dat'

        if not os.path.exists(fname):
            print(f'Running EZmock with parameters: {param}')
            # Run EZmock
            ez.populate_tracer_to_file(rho_c, rho_exp, pdf_base, sigma_v, ntracer, fname, rsd_fac=rsd_fac)

        fnames.append(fname)
            
        # Measure clustering statistics
        # pyc.run(fname, Lbox)

    # Plot clustering statistics
    # pyc.plot(fnames)

# %%
params = [
  [0, 3, 0.48, 400],
]

pyc = None
run_and_plot_EZmock(ez, pyc, params)

# %%



