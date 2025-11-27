# %%
# !source /global/common/software/desi/users/adematti/cosmodesi_environment.sh main 
from pypower import CatalogFFTPower, mpi
import numpy as np


# %%
## settings for pypower
mpicomm = mpi.COMM_WORLD
mpiroot = None # input positions/weights scattered on all processes
Lbox = 2000
Nmesh = 256
kmax = Nmesh*np.pi/Lbox
kedges = np.linspace(0, kmax, Nmesh//2+1)
edges = (kedges, np.linspace(-1., 1., 5))
ells=(0,2)


# %%
def run_pypower_redshift(x, y, z, Lbox=Lbox, Nmesh=Nmesh, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot):    
    ## positions
    pos = np.vstack((x, y, z)).T
    weight = np.ones(len(pos))
    result = CatalogFFTPower(pos, data_weights1=weight, boxsize=Lbox, nmesh=Nmesh, 
                         resampler='tsc', interlacing=3, ells=ells, 
                         los='z', edges=edges,  position_type='pos', mpicomm=mpicomm, mpiroot=mpiroot)
    poles = result.poles
    return poles

# %%
# path2ez='out/EZmock_L1000_N256_fnl1500_c0_e3_b0.48_v400.dat'
# data2ez = np.loadtxt(path2ez)
# x_ez, y_ez, z_ez = data2ez[:,0], data2ez[:,1], data2ez[:,2]
# poles_ez = run_pypower_redshift(x_ez, y_ez, z_ez, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)

# path2ez2='out/EZmock_L1000_N256_fnl1200_c0_e3_b0.48_v400.dat'
# data2ez2 = np.loadtxt(path2ez2)
# x_ez2, y_ez2, z_ez2 = data2ez2[:,0], data2ez2[:,1], data2ez2[:,2]
# poles_ez2 = run_pypower_redshift(x_ez2, y_ez2, z_ez2, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)

# path2ez500='out/EZmock_L1000_N256_fnl500_c0_e3_b0.48_v400.dat'
# data2ez500 = np.loadtxt(path2ez500)
# x_ez500, y_ez500, z_ez500 = data2ez500[:,0], data2ez500[:,1], data2ez500[:,2]
# poles_ez500 = run_pypower_redshift(x_ez500, y_ez500, z_ez500, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)
path2ez500='out/EZmock_L1000_N256_fnl500_c1.2_e8_b0.35_v480.dat'
data2ez500 = np.loadtxt(path2ez500)
x_ez500, y_ez500, z_ez500 = data2ez500[:,0], data2ez500[:,1], data2ez500[:,2]
poles_ez500 = run_pypower_redshift(x_ez500, y_ez500, z_ez500, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)

# path2ez600='out/EZmock_L1000_N256_fnl600_c0_e3_b0.48_v400.dat'
# data2ez600 = np.loadtxt(path2ez600)
# x_ez600, y_ez600, z_ez600 = data2ez600[:,0], data2ez600[:,1], data2ez600[:,2]
# poles_ez600 = run_pypower_redshift(x_ez600, y_ez600, z_ez600, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)
path2ez600='out/EZmock_L1000_N256_fnl600_c1.2_e8_b0.35_v480.dat'
data2ez600 = np.loadtxt(path2ez600)
x_ez600, y_ez600, z_ez600 = data2ez600[:,0], data2ez600[:,1], data2ez600[:,2]
poles_ez600 = run_pypower_redshift(x_ez600, y_ez600, z_ez600, Lbox=1000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)

# %%
sim='Abacus_pngbase_c302_ph000'
redshift = 3.0
hod='_dv'
path2ab=f"/pscratch/sd/s/siyizhao/desi-dr2-hod/mocks/{sim}/z{redshift:.3f}/galaxies_rsd{hod}/QSOs.dat"
data2ab = np.loadtxt(path2ab, skiprows=15)
x_ab, y_ab, z_ab = data2ab[:,0], data2ab[:,1], data2ab[:,2]
poles_ab = run_pypower_redshift(x_ab, y_ab, z_ab, Lbox=2000, Nmesh=256, edges=edges, ells=ells, mpicomm=mpicomm, mpiroot=mpiroot)


# %%
from matplotlib import pyplot as plt

# %%
plt.plot(*poles_ab(ell=0, return_k=True, complex=False), label='AbacusHOD (fnl=100)')
# plt.plot(*poles_ez(ell=0, return_k=True, complex=False), label='EZmock (fnl=1500)')
# plt.plot(*poles_ez2(ell=0, return_k=True, complex=False), label='EZmock (fnl=1200)')
plt.plot(*poles_ez500(ell=0, return_k=True, complex=False), label='EZmock (fnl=500)')
plt.plot(*poles_ez600(ell=0, return_k=True, complex=False), label='EZmock (fnl=600)')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('k [h/Mpc]')
plt.ylabel('P0(k) [(Mpc/h)$^3$]')
plt.legend()
plt.savefig('poles_comparison_ezmock_abacus.png')

# %%



