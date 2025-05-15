import numpy as np
from matplotlib import pyplot as plt
import emcee
import corner

# to not run the samplers and save times, the result can be found in the posteriorBayesGraphs directory

# importing dataset
datas = np.load("../solutions/transient.npy")
#print(datas)
#print(datas.shape)
#print(datas.T[0])

# divide by columns the datas in three arrays
time = datas.T[0]
flux = datas.T[1]
sigma_flux = datas.T[2]

#plt.scatter(time, flux, marker="o", edgecolors="black", color="none", ls="",label="datas") cool dots
plt.errorbar(time, flux, yerr=sigma_flux, marker="o", ls="", color="lightblue", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.legend()
plt.xlabel("time")
plt.ylabel("flux")
plt.show()

# defining the model
def model(theta, t):
    A, b, t0, alp = theta
    return np.where(t<t0, b, b + A * np.exp(-alp * (t - t0)))
    # if t < t0:
    #     return b
    # if t >= t0:
    #     return b + A * np.exp(-alp * (t - t0))
    # return None

'''
# try to "fit" by hand
t0_quick=50
A_quick=5
b_quick=10
alpha_quick=0.1

theta_quick= np.array([A_quick,b_quick,t0_quick,alpha_quick])

tgrid = np.linspace(time.min(), time.max(), 100)
plt.plot(tgrid, model(theta_quick, tgrid), ls="-", color="red", label="handfit")
plt.errorbar(time, flux, yerr=sigma_flux, marker="o", ls="", color="lightblue", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.legend()
plt.xlabel("time")
plt.ylabel("flux")
plt.show()
'''

# priors
bmin, bmax = 0, 50
Amin, Amax = 0, 50
t0min, t0max = 0, 100
alphaMin, alphaMax = np.exp(-5), np.exp(5)

# definyng things for emcee - define all the relevant functions
# def Likelihood(x, sigma, data):
#     # Gaussian likelihood
#     return np.prod(np.exp(-(data-x)**2 /2 /sigma**2))
#
# def Prior(x):
#     return 1.0 / 10   # flat: it cancels out and has no effect
#
# def myPosterior(x, sigma, data):
#     return Likelihood(x, sigma, data) * Prior(x)
#
# # emcee wants ln of posterior pdf
# def myLogPosterior(x, sigma, data):
#     return np.log(myPosterior(x, sigma, data))

# ----------------------------------------------------------------------------------------------------------- right ones
def LogLikelihood(theta, data, model=model):
    x, y, sigma_y = data.T
    y_fit = model(theta, x)
    return -0.5 * np.sum((y - y_fit) ** 2 / sigma_y ** 2)

## prior is proportional to 1/alpha
def Logprior(theta):
    A, b, t0, alpha = theta
    if Amin < A < Amax and bmin < b < bmax and t0min < t0 < t0max and alphaMin < alpha < alphaMax:
        return 0.0 + 0.0 + 0.0 - np.log(alpha)
    return -np.inf

def LogPosterior(theta, data, model=model):
    return LogLikelihood(theta, data, model) + Logprior(theta)

ndim = 4  # number of parameters in the model
nwalkers = 20  # number of MCMC walkers
nsteps = int(1e4)  # number of MCMC steps to take for each walker

t0_quick=50
A_quick=5
b_quick=10
alpha_quick=0.1
theta_quick= np.array([A_quick,b_quick,t0_quick,alpha_quick])
starting_guesses = theta_quick + 1e-1* np.random.randn(nwalkers, ndim)
print(starting_guesses.shape)

sampler = emcee.EnsembleSampler(nwalkers, ndim, LogPosterior, args=[datas, model])
sampler.run_mcmc(starting_guesses, nsteps)

# plot the chains
fig, axes = plt.subplots(4, figsize=(10, 7), sharex=True)
samples = sampler.get_chain()
labels = ["A","b","t0","alpha"]
for i in range(ndim):
    ax = axes[i]
    ax.plot(samples[:, :, i], "k", alpha=0.3)
    ax.set_xlim(0, len(samples))
    ax.set_ylabel(labels[i])
    ax.yaxis.set_label_coords(-0.1, 0.5)

axes[-1].set_xlabel("step number")
plt.show()

# get the correlation length
tau = sampler.get_autocorr_time()
print("Correlation lenghts = ", tau)

# set the burn-in (3 times the correlation lengths) +  thin the chain (by the largest correlation length)
flat_samples = sampler.get_chain(discard=3*int(max(tau)), thin=int(max(tau)), flat=True)
print(flat_samples.shape)

# plotting the results
fig = corner.corner(flat_samples, labels=labels, levels=[0.68,0.95])
plt.show()

# plotting the models
chosen_samples= flat_samples[np.random.choice(len(flat_samples),size=30)]
tgrid = np.linspace(0, 100, 100)

for chosen_theta in chosen_samples:
    ygrid = model(chosen_theta, tgrid)
    plt.plot(tgrid, ygrid, alpha=0.3, c='gray')

plt.errorbar(time, flux, yerr=sigma_flux, marker="o", ls="", color="lightblue", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.xlabel("time")
plt.ylabel("flux")
plt.show()
# da committare