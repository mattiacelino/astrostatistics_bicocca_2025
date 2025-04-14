import sklearn
import numpy as np
from matplotlib import pyplot as plt

# Loading the file
file = np.load("../solutions/formationchannels.npy")
#print(file)

# Fitting
model = sklearn.mixture.GaussianMixture(1)
model.fit(file)
print(model.aic(file)) # the lower the better, says the support page of sklearn https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html

# Fitting from 1 to 10 Gaussians
N = [1,2,3,4,5,6,7,8,9,10]
aics = []
for n in N:
    model = sklearn.mixture.GaussianMixture(n)
    model.fit(file)
    aics.append(model.aic(file))

plt.plot(N, aics, ls="", marker=".", color="dodgerblue")
plt.xlabel("# of gaussians")
plt.ylabel("AIC")
plt.show()

print("Lowest AIC = ", np.min(aics))
index = np.argsort(aics)[0]
print("Corresponding N = ", N[index])

# plot the datas
plt.hist(file, bins=int(10*np.log10(len(file))), histtype="step", density=True, label="datas")

# plot the best model
M_best = sklearn.mixture.GaussianMixture(N[index])
M_best.fit(file)
t = np.linspace(0, 60, 1000)
logprob = M_best.score_samples(t.reshape(-1, 1))
pdf = np.exp(logprob)

plt.plot(t, pdf, ls="-", color="blue", label="N = " + str(N[index]))
plt.legend()
plt.show()

# plot other models, just for fun
for i in [1,3,7,10]:
    M_best = sklearn.mixture.GaussianMixture(i)
    M_best.fit(file)
    t = np.linspace(0, 60, 1000)
    logprob = M_best.score_samples(t.reshape(-1, 1))
    pdf = np.exp(logprob)

    plt.plot(t, pdf, ls="-", label="N = " + str(i))

plt.hist(file, bins=int(10*np.log10(len(file))), histtype="step", density=True, label="datas")
plt.legend()
plt.show()
