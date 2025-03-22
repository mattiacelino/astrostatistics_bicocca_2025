from astroML.datasets import fetch_dr7_quasar
from matplotlib import pyplot as plt
import numpy as np
import scipy

# Fetch the quasar data
data = fetch_dr7_quasar()

# select the first 10000 points
#data = data[:10000]

z = data['redshift']
plt.hist(z, bins=30, histtype='step', density=True, label="original datas")
#plt.show()

# With rejecton sampling
counts, bins = np.histogram(z, bins=30, density=True)
disth = scipy.stats.rv_histogram((counts, bins))  # serve per prendere la distribuzione

N = 1000
x = np.random.uniform(0,6, N)
y = np.random.uniform(0,np.max(counts), N)

goodpoints = x[y <= disth.pdf(x)]
plt.hist(goodpoints, bins=30, histtype='step', density=True, label="rejection sampling")
plt.legend()
plt.show()
