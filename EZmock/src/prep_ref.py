
import numpy as np
import os
import yaml
import catinbox as cb
import sys; sys.path.append("/global/homes/s/siyizhao/lib/pyfcfc")
from pyfcfc.boxes import py_compute_cf

LBOX = 2000.0
NGRID = 512
ncpu = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))

def load_config(path='conf/fitEZ.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def read_Abacus_mock(dir = 'mocks', sim = 'AbacusSummit_base_c000_ph000', z = 2.000, hod = '_dv', tracer = 'QSO'):
    MOCK_IN = f"/pscratch/sd/s/siyizhao/desi-dr2-hod/{dir}/{sim}/z{z:.3f}/galaxies_rsd{hod}/{tracer}s.dat"
    print(f"Loading mock from {MOCK_IN}")
    with open(MOCK_IN, 'r') as f:
        it = iter(f)
        for line in it:
            if not line.lstrip().startswith('#'):
                break
        data = np.loadtxt(it)
    x = data[:,0]
    y = data[:,1]
    z_rsd = data[:,2]
    num = x.shape[0]
    return num, x, y, z_rsd

## measure and save reference clustering ---------------------------------------

def measure_pk(xref, yref, zref, path=None):
    CONFIG = load_config()
    item = CONFIG['clustering']['pk']
    pkcfg = {
        'ngrid': NGRID,
        'lbox': LBOX,
        'kmin': item['kmin'],
        'kmax': item['kmax'],
        'nbin': item['nbin'],
        'l0': True,
        'l2': True,
        'l4': True,
        'assign': 'CIC',
        'intlace': True,
        'ncpu': ncpu,
        'verbose': False,
    }
    pkref = cb.powspec_box(xref, yref, zref, **pkcfg)
    if path is not None:
        kcen = pkref.k
        kmin = pkref.kedge[:-1]
        kmax = pkref.kedge[1:]
        kavg = pkref.kmean
        nmod = pkref.nmode
        P_0 = pkref.p0
        P_2 = pkref.p2
        P_4 = pkref.p4
        if P_4 is None:
            P_4 = np.zeros_like(P_0)
            print("Warning: P_4 is None, set to zero.")
        np.savetxt(path, np.column_stack((kcen, kmin, kmax, kavg, nmod, P_0, P_2, P_4)), header='kcen kmin kmax kavg nmod P_0 P_2 P_4')


fcfccfg = 'conf/fcfc_ref.conf'
devnull = os.open(os.devnull, os.O_WRONLY)
def get_xi(xs, ys, zs, smin, smax, nbin, nmu=100, conf=fcfccfg):
    # 同步实现：直接在当前进程调用 py_compute_cf
    # 在需要静默底层 C 扩展输出时，临时重定向底层 stdout/stderr 到 devnull
    old_stdout_fd = None
    old_stderr_fd = None
    try:
        # 备份 stdout/stderr
        old_stdout_fd = os.dup(1)
        old_stderr_fd = os.dup(2)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)

        data = np.column_stack((xs, ys, zs)).astype(np.float32)
        w = np.ones(data.shape[0], dtype=np.float32)
        sedgs = np.linspace(smin, smax, nbin + 1)
        result = py_compute_cf([data, data], [w, w], sedgs, None, nmu, conf=conf)
        return result
    finally:
        # 恢复 stdout/stderr
        try:
            if old_stdout_fd is not None:
                os.dup2(old_stdout_fd, 1)
                os.close(old_stdout_fd)
            if old_stderr_fd is not None:
                os.dup2(old_stderr_fd, 2)
                os.close(old_stderr_fd)
        except Exception:
            pass

def measure_xi(xref, yref, zref, path=None):
    CONFIG = load_config()
    item = CONFIG['clustering']['xi']
    xicfg = {
        'smin': item['smin'],
        'smax': item['smax'],
        'nbin': item['nbin'],
    }
    xiref = get_xi(xref, yref, zref, **xicfg)
    if path is not None:
        s = xiref['s']
        smin = xiref['pairs']['smin'][:,0]
        smax = xiref['pairs']['smax'][:,0]
        xi0 = xiref['multipoles'][0][0]
        xi2 = xiref['multipoles'][0][1]
        np.savetxt(path, np.column_stack((s, smin, smax, xi0, xi2)), header='s smin smax xi0 xi2')
    return xiref


def measure_bk(xref, yref, zref, path=None):
    CONFIG = load_config()
    item = CONFIG['clustering']['bk']
    bkcfg = {
        'ngrid': NGRID,
        'lbox': LBOX,
        'k1': item['k1'],
        'dk1': item['dk1'],
        'k2': item['k2'],
        'dk2': item['dk2'],
        'nbin': item['nbin'],
        'assign': 'CIC',
        'intlace': True,
        'ncpu': ncpu,
        'verbose': False,
    }
    bkref = cb.bispec_box(xref, yref, zref, **bkcfg)
    if path is not None:
        theta = bkref.a
        theta_mean = bkref.amean
        k3 = bkref.k3
        modes = bkref.nmode
        B = bkref.b
        Q = bkref.q
        np.savetxt(path, np.column_stack((theta, theta_mean, k3, modes, B, Q)), header='theta theta_mean k3 modes B Q')

def save_ref_clus(xref, yref, zref, path2pk, path2xi, path2bk):
    measure_pk(xref, yref, zref, path=path2pk)
    measure_xi(xref, yref, zref, path=path2xi)
    measure_bk(xref, yref, zref, path=path2bk)