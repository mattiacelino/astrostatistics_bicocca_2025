from sklearn import datasets
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import Isomap

# DIMENSIONALITY REDUCTION

digits = datasets.load_digits()
print(digits.images.shape)
print(digits.keys())

print(digits.DESCR)

fig, axes = plt.subplots(7,7, figsize=(10, 10))
fig.subplots_adjust(hspace=0.1, wspace=0.1)

mychoices = np.random.choice(digits.images.shape[0],100)

for i, ax in enumerate(axes.flat):
    ax.imshow((digits.images[mychoices[i]]), cmap='binary')
    ax.text(0.05, 0.05, str(digits.target[mychoices[i]]),transform=ax.transAxes, color='green', fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])

plt.show()

iso = Isomap(n_components=2)
data_projected = iso.fit_transform(digits.data)
print(digits.data.shape, " is reduced to ", data_projected.shape)

#From: https://gist.github.com/jakevdp/91077b0cae40f8f8244a
def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""
    base = plt.colormaps[base_cmap]
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

# Plot all of the data points in the two projected dimensions.
# Color the points by their labels.
plt.scatter(data_projected[:,0], data_projected[:,1], c=digits.target, edgecolor='none', alpha=0.5, cmap=discrete_cmap(10,'nipy_spectral'));

# Add the color bar
plt.colorbar(label='digit label', ticks=range(10))

# Make it clear which color goes with which label
plt.clim(-0.5, 9.5)
plt.show()

# CLASSIFICATION NOW
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# taking 80% of the data as a training set
Xtrain, Xtest, ytrain, ytest = train_test_split(digits.data, digits.target, random_state=2, train_size=0.8)
print("Shapes of train and test: ", Xtrain.shape, Xtest.shape)

clf = LogisticRegression(penalty='l2', max_iter=2000,solver='sag')
clf.fit(Xtrain, ytrain)

ypred = clf.predict(Xtest)
print("Accuracy prediction of test = ", accuracy_score(ytest, ypred))

ypredtrain = clf.predict(Xtrain)
print("Accuraty prediction of train (of course it's = 1): ", accuracy_score(ytrain, ypredtrain))

# Confusion matrix
print("Confusion matrix:\n", confusion_matrix(ytest, ypred))

