import numpy as np
from matplotlib import pyplot as plt
import astropy.visualization.hist
from sklearn.neighbors import KernelDensity
from scipy import stats

# Define quantities
def f():
    spin = np.random.uniform(0,1,size=1)
    func = np.sqrt((1 + np.sqrt(1 - spin**2)) / 2)
    return func[0]

sigma = 0.02
mu = 1

M_irr = []

for i in range(0,1000):
    M = np.random.normal(mu, sigma, size=1)
    mass_irr = M[0] * f()
    M_irr.append(mass_irr)

# 1. plot histograms with different methods
plt.hist(M_irr, bins=int(10*np.log10(len(M_irr))), histtype="step", density=True, label="sturges")
astropy.visualization.hist(M_irr, bins="scott", histtype="step",density=True,label="scott")
astropy.visualization.hist(M_irr, bins="freedman", histtype="step",density=True,label="freedman")
plt.legend()
plt.show()

# 2. KDE
M_irr = np.array(M_irr)
xgrid = np.linspace(M_irr.min(),M_irr.max(),1000)

def kde_sklearn(data, bandwidth = 1.0, kernel="linear"):
    kde_skl = KernelDensity(bandwidth = bandwidth, kernel=kernel)
    kde_skl.fit(data[:, np.newaxis])
    log_pdf = kde_skl.score_samples(xgrid[:, np.newaxis]) # sklearn returns log(density)
    return np.exp(log_pdf)

PDFtophat = kde_sklearn(M_irr,bandwidth=0.005,kernel="gaussian")
plt.plot(xgrid,PDFtophat, label="gaussian")

PDFtophat = kde_sklearn(M_irr,bandwidth=0.01,kernel="epanechnikov")
plt.plot(xgrid,PDFtophat, label="epanechnikov")
plt.legend()
plt.show()

# check the limits: large sigma and small sigma
def m_irr_func(s):
    m_irr = []
    for n in range(0, 1000):
        m = np.random.normal(mu, s, size=1)
        mass_irr = m[0] * f()
        m_irr.append(mass_irr)
    return m_irr

small_sigma = m_irr_func(0.0001)
plt.hist(small_sigma, bins=int(10*np.log(len(small_sigma))), histtype="step", density=True, label="small σ")
plt.legend()
plt.show()

large_sigma = m_irr_func(1000)
plt.hist(large_sigma, bins=int(10*np.log(len(large_sigma))), histtype="step", density=True, label="large σ")
plt.legend()
plt.show()

# 3. + 4. Compute KS distance

# First I calculate the three distributions
def M(sigma, N):
    return np.random.normal(mu, sigma, size=N)

def f_sigmas(N):
    spin = np.random.uniform(0,1,size=N)
    func = np.sqrt((1 + np.sqrt(1 - spin**2)) / 2)
    return func

# compute and plot KS distances
N = 100_000
KS_test_M = [] # KS distances between M_irr and M
KS_test_f = [] # KS distances between M_irr and f
sigmas = np.logspace(-5,5,10)
for n in sigmas:
    M_distribution = M(n, N)
    f_distribution = f_sigmas(N)
    mIRR = m_irr_func(n)

    KS_test_M.append(stats.ks_2samp(M_distribution, mIRR))
    KS_test_f.append(stats.ks_2samp(f_distribution, mIRR))

KS_test_M = np.array(KS_test_M)
KS_test_f = np.array(KS_test_f)

plt.plot(sigmas, KS_test_M[:,0], ls="-", label="KS_dist(M_irr, M)")
plt.plot(sigmas, KS_test_f[:,0], ls="-", label="KS_dist(M_irr, f)")
plt.legend()
plt.xscale("log")
plt.show()
