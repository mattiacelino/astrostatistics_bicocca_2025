import numpy as np
from matplotlib import pyplot as plt
import scipy.stats

deaths = np.array([0,    1,  2, 3, 4])
groups = np.array([109, 65, 22, 3, 1])
frequency = groups / groups.sum()

plt.plot(deaths, frequency, marker="^", color="dodgerblue", ls="")
plt.show()