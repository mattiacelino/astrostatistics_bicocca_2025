import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm

# generate 10 measures of the position of the quasar
mu = 1
sigma = 0.2
gaussian = np.random.normal(mu, sigma, 5)
print(gaussian)

# calculate each likelihood
t = np.linspace(0,2,100)

L = []
for i in gaussian:
    L.append(norm.pdf(t, i, sigma))

np.array(L)
#print(L)

# plot each likelihood
for l in L:
    plt.plot(t, l, ls="-")

# plot the product
product = 1
for l in L:
    product *= l
#print(product)
plt.plot(t,product, ls="--")
plt.show()  # show all

# print the maximum solution
index = np.argsort(product)[-1]  # find where, on the x-axis, is the maximum of the product
print(index)
print("max likelyhood = ", t[index])  # print the corresponding value on the x-axis
print("extimator = ", np.mean(gaussian))
