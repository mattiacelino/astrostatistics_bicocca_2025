import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm

# PART 1 ---------------------------
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
index = np.argsort(product)[-1]  # find the index of the maximum of the product (the last one, once sorted)
#print(index)
print("max likelyhood = ", t[index])  # print the corresponding value on the x-axis
print("extimator = ", np.mean(gaussian), "\n\n")

# PART 2 ---------------------------

# 2nd order differentiation of logLikelyhood
result = np.diff(np.log(product), n=2)
# divide by Δθ^2
result /= (t[1] - t[0])**2
# multiply by -1
result *= -1
# take the square root
result = np.sqrt(result[index])
print("result from differentiation = ", 1/result)
print("result from Fischer = ", sigma/np.sqrt(len(gaussian)))

# plot a gaussian at measured mu but with this error (result)
plt.plot(t, product, ls="--", color="dodgerblue", label="datas")
C = 1.0  # sometimes it can be necessary to normalize to visually overlap the two
plt.plot(t, C * norm.pdf(t, t[index], 1/result), ls="--", color="tomato", label="estimated")
plt.legend()
plt.show()
