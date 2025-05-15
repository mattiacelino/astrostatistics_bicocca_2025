import numpy as np
from matplotlib import pyplot as plt
import corner
import dynesty
import scipy
from dynesty import utils as dyfunc
from dynesty import plotting as dyplot

# to not run the samplers and save times, the result can be found in the posteriorBayesGraphs directory

# importing dataset
datas = np.load("../solutions/transient.npy")
time = datas.T[0]
flux = datas.T[1]
sigma_flux = datas.T[2]

plt.errorbar(time, flux, yerr=sigma_flux, marker="o", ls="", color="lightblue", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.legend()
plt.xlabel("time")
plt.ylabel("flux")
plt.show()

# defining the models
def model(theta, t):
    A, b, t0, alp = theta
    return np.where(t<t0, b, b + A * np.exp(-alp * (t - t0)))

# defining parameters
bmin, bmax = 0, 50
t0min, t0max = 0, 100
Amin, Amax = 0, 50
alphamin, alphamax = np.exp(-5), np.exp(5)
sigWmin, sigWmax = np.exp(-2), np.exp(2)

# nested sample

ndim = 4

def LogLikelihood(theta, data):
    x, y, sigma_y = data.T
    y_fit = model(theta, x)
    return -0.5 * np.sum((y - y_fit) ** 2 / sigma_y ** 2)


def ptform(u, model):
    """Transforms the uniform random variables `u ~ Unif[0., 1.)`
    to the parameters of interest."""

    x = np.array(u)  # copy u

    x[0] = scipy.stats.uniform(loc=Amin, scale=Amax - Amin).ppf(u[0])
    x[1] = scipy.stats.uniform(loc=bmin, scale=bmax - bmin).ppf(u[1])
    x[2] = scipy.stats.uniform(loc=t0min, scale=t0max - t0min).ppf(u[2])

    # since I want to reuse this:
    if model == 'burst':
        x[3] = scipy.stats.loguniform.ppf(u[3], alphamin, alphamax)
    elif model == 'gprofile':
        x[3] = scipy.stats.loguniform.ppf(u[3], sigWmin, sigWmax)
    return x

# defining and running the sampler
sampler = dynesty.NestedSampler(LogLikelihood, ptform, ndim,logl_args=[datas],ptform_args=['burst'],nlive=300)
sampler.run_nested()
sresults = sampler.results
print("\n--------- Results summary ---------\n",sresults.summary())

# plotting the results
rfig, raxes = dyplot.runplot(sresults)
plt.show()

tfig, taxes = dyplot.traceplot(sresults)
plt.show()

# plotting corner plots
samples = sresults.samples  # samples
weights = np.exp(sresults.logwt - sresults.logz[-1])  # normalized weights

labels = ["A","b","t0","alpha"]

samples_equal = dyfunc.resample_equal(samples, weights)
corner.corner(samples_equal,labels=labels)
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# gaussian profile model
def gaussianProfile(theta, t):
    A, b, t0, sigW = theta
    return b + A * np.exp(-((t -t0)**2 / 2*sigW**2))

def LogLikelihood(theta, data):
    x, y, sigma_y = data.T
    y_fit = gaussianProfile(theta, x)
    return -0.5 * np.sum((y - y_fit) ** 2 / sigma_y ** 2)

# running the sampler
sampler = dynesty.NestedSampler(LogLikelihood, ptform, ndim,logl_args=[datas],ptform_args=['gprofile'],nlive=300)
sampler.run_nested()
sresults2 = sampler.results

print("\n--------- Results summary ---------\n",sresults2.summary())

# plotting the results
rfig, raxes = dyplot.runplot(sresults2)
plt.show()

tfig, taxes = dyplot.traceplot(sresults2)
plt.show()

# plotting corner plots
samples = sresults2.samples  # samples
weights = np.exp(sresults2.logwt - sresults2.logz[-1])  # normalized weights

labels = ["A","b","t0","sigmaW"]

samples_equal = dyfunc.resample_equal(samples, weights)
corner.corner(samples_equal,labels=labels)
plt.show()

# print the odds ratio between the model to know which is better (confronting with Jeffrey's scale)
print("\nModels ratio = ",np.exp(sresults.logz[-1])/np.exp(sresults2.logz[-1]))
