import numpy as np
from matplotlib import pyplot as plt
import scipy.stats

# I = σ * (np.sqrt(np.pi / 2)) * ∫ x^3 * p(x)
# p(x) --> gaussiana

sigma = 3.0 #fixed sigma
N = 1000 #number of MonteCarlo generated
gaussiana = scipy.stats.norm(loc=0,scale=sigma) #Gaussian func
generated = np.abs(gaussiana.rvs(N)) #N numbers generated according to Gaussian

plt.hist(generated,density=True,bins=30,color="dodgerblue") #histogram with generated numbers
plt.show() #for showing the graph

I = sigma * (np.sqrt(np.pi / 2)) * np.mean(generated**3) #integral
result = 2 * sigma**4 #2σ^4
print("integral with MonteCarlo = ", I)
print("known result = ", result)

def montecarlo(num):
    generated = np.abs(gaussiana.rvs(num))
    I = sigma * (np.sqrt(np.pi / 2)) * np.mean(generated ** 3)
    return I

#Now do it a lot of times.
N = [1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]
totals = []
for i in N:
    totals.append(montecarlo(i))

plt.hlines(result, 1, 100_000_000, color="limegreen", linestyle="-", label="known result")
plt.plot(N, totals, marker="", linestyle="-", color="tomato", label="MonteCarlo results")
plt.yscale("log")
plt.xscale("log")
plt.legend()
plt.show()