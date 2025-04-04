import numpy as np
from matplotlib import pyplot as plt

# generate 10 measures of the position of the quasar
mu = 1
sigma = 0.2
gaussian = np.random.normal(mu, sigma, 5)
print(gaussian)

# plot each likelihood

def likelihood(x, mu, sig):
    return (1/(sig * np.sqrt(2 * np.pi))) * np.exp( -(x - mu)**2 / (2 * sig**2) )


t = np.linspace(0,2,100)
for i in gaussian:
    plt.plot(likelihood(t, i, sigma), ls="-")

# plot the product
product = 1
for i in gaussian:
    product *= likelihood(t, i, sigma)
plt.plot(product, ls="--")

plt.show() # show all

# plot the maximum solution
