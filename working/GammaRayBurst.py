import numpy as np
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

datas = np.loadtxt("GRB_datas.txt", dtype="str", unpack=True)
with open("GRB_datas.txt") as f:
    names = np.array([n.strip().replace(" ","_") for n in f.readlines()[1].replace("#","").replace("\n","").lstrip().split('    ') if n.strip()!=''])

print("Columns: ", names)

T90, fluence, redshift = np.loadtxt("GRB_datas.txt", usecols=[6, 9, 11], unpack=True)

plt.errorbar(T90[fluence!=-999], fluence[fluence!=-999], marker="o", ls="", color="lightblue", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("T90")
plt.ylabel("fluence")
plt.show()

plt.hist(T90, histtype="step", bins=np.logspace(-2,3,100), color="limegreen")
plt.xscale("log")
plt.show()

# plt.hist(fluence, histtype="step", bins=np.linspace(0,100,100), color="dodgerblue")
# plt.xscale("log")
# plt.show()
#
# plt.hist(redshift, histtype="step", bins=np.linspace(0,100,100), color="tomato")
# plt.xscale("log")
# plt.show()

plt.errorbar(T90[fluence!=-999], redshift[fluence!=-999], marker="o", ls="", color="tomato", ecolor="black", capsize=3, markeredgecolor="black", label="datas")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("T90")
plt.ylabel("redshift")
plt.show()

# searching for clusters in T90 datas

# Reshape for scikit-learn
# I want to fit the log of T90...
lT90 = np.log10(T90)
# Some cleaning...
lT90=lT90[~np.isnan(lT90)]
# Reshape for scikit-learn
skT90 = lT90[:,np.newaxis]

clf = KMeans(n_clusters=2, n_init='auto') # 2 because it seems like two Gaussians-like funcs
clf.fit(skT90)

centers = clf.cluster_centers_ #location of the clusters
centers = 10**np.squeeze(centers)
print("centers with kMeans: ", centers) #in seconds

# plot the centers in the histogram and the separation line (edge)
labels = clf.predict(skT90)
edge = 10**(np.mean([max(skT90[labels==0]), min(skT90[labels==1])]))
print("edge with kMeans: ", edge)

plt.hist(T90, histtype="step", bins=np.logspace(-2,3,100), color="limegreen")
plt.axvline(centers[0], ls="--", color="red")
plt.axvline(centers[1], ls="--", color="red")
plt.axvline(edge, ls="-", color="red")
plt.xscale("log")
plt.show()

# Try another method: Gaussian Mixture
gmm = GaussianMixture(2).fit(skT90)
means = 10**np.squeeze(gmm.means_)
print("\ncenters with Gaussian Mixture: ", means)
plt.hist(T90, histtype="step", bins=np.logspace(-2,3,100), color="limegreen")
plt.axvline(means[0], ls="--", color="red")
plt.axvline(means[1], ls="--", color="red")
plt.xscale("log")
plt.show()
