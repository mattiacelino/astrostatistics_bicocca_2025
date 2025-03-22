import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

deaths = np.array([0,    1,  2, 3, 4])
groups = np.array([109, 65, 22, 3, 1])
frequency = groups / groups.sum()

def poisson(k, mu):
    return (mu**k * np.exp(-mu)) / k

(args, var) = curve_fit(poisson, deaths, frequency, absolute_sigma=True)
t = np.linspace(deaths.min(), deaths.max(), 1000)
plt.plot(deaths, frequency, marker="^", color="dodgerblue", ls="")
plt.plot(t, poisson(t, *args), ls="--", color="blue", label="fit")
plt.legend()
plt.show()