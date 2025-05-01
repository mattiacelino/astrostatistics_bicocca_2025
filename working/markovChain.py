import random
import numpy as np
from matplotlib import pyplot as plt

# Func for the cycle (not so efficient but does the job)
# rainy = 0
# sunny = 1
def nextDay(day):
    prob = random.randint(0,100)
    if day == 0: # rainy
        if prob <= 50:
            return 0 # rainy
        elif prob > 50:
            return 1 # sunny
    if day == 1: # sunny
        if prob <= 90:
            return 1 # sunny
        elif prob > 90:
            return 0 # rainy


today = 0  # rainy the first day
days = []
N = 10_000

for d in range(0,N):
    newDay = nextDay(today)
    today = newDay
    days.append(today)

days = np.array(days)
t = np.linspace(1, N, num=N)
plt.plot(t, days.cumsum()/t, ls="-", color="dodgerblue")
plt.legend()
plt.xlabel("days")
plt.ylabel("sunny/total")
plt.show()

# histogram
dist = days.cumsum()/t
#print(dist)
plt.hist(dist, bins=int(10*np.log10(len(dist))), histtype="step", color="limegreen", density=True)
print("mean = ", np.mean(dist))
print("median = ", np.median(dist))
print("min = ", dist.min(), " and max = ", dist.max())
plt.show()

# discard burn-in phase with histogram
burn = 2_500
dist = dist[burn:]
plt.hist(dist, bins=int(10*np.log10(len(dist))), histtype="step", color="limegreen", density=True, label=str(burn))
#plt.hist(dist, bins=300, histtype="step", color="limegreen", density=True) changed bins number to double-check with solution
print("\nBURN-IN: " + str(burn) + "\nmean = ", np.mean(dist))
print("median = ", np.median(dist))
print("min = ", dist.min(), " and max = ", dist.max())
#plt.title("burn in at " + str(burn))
#plt.show()

burn = 3_500
dist = dist[burn:]
plt.hist(dist, bins=int(10*np.log10(len(dist))), histtype="step", color="tomato", density=True, label=str(burn))
#plt.hist(dist, bins=300, histtype="step", color="limegreen", density=True) changed bins number to double-check with solution
print("\nBURN-IN: " + str(burn) + "\nmean = ", np.mean(dist))
print("median = ", np.median(dist))
print("min = ", dist.min(), " and max = ", dist.max())
#plt.title("burn in at " + str(burn))
#plt.show()

burn = 1_000
dist = dist[burn:]
plt.hist(dist, bins=int(10*np.log10(len(dist))), histtype="step", color="dodgerblue", density=True, label=str(burn))
#plt.hist(dist, bins=300, histtype="step", color="limegreen", density=True) changed bins number to double-check with solution
print("\nBURN-IN: " + str(burn) + "\nmean = ", np.mean(dist))
print("median = ", np.median(dist))
print("min = ", dist.min(), " and max = ", dist.max())
#plt.title("burn in at " + str(burn))
plt.legend()
plt.show()

# repeat again everything
def trace_plot(arrayTotal):
    today = 0  # rainy the first day
    days = []
    N = 10_000

    for d in range(0,N):
        newDay = nextDay(today)
        today = newDay
        days.append(today)

    days = np.array(days)
    t = np.linspace(1, N, num=N)
    plt.plot(t, days.cumsum()/t, ls="-")
    arrayTotal.append(days)

totals = []
for i in range(0,4):
    trace_plot(totals)

#totals = np.array(totals)
plt.hlines(np.mean(totals), 0, N, ls="--", color="black", label="mean")
plt.legend()
plt.xlabel("days")
plt.ylabel("sunny/total")
plt.show()
