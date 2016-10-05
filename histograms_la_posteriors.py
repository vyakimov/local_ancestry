import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir("/projects/ingo/local_ancestry/viya_tmp/intermediate_data/")
individuals = 1388
n=50

posteriors = pd.Series()
for individual in np.random.choice(np.arange(1,individuals+1),n,replace=False):
    for chromosome in range(1,23):
        print "doing {}:{}".format(individual, chromosome)
        p = pd.read_table("./rfmix_out/chr{}.3.ForwardBackward.txt".format(chromosome),
                          usecols=[individual - 1, individual + 1], header=None, sep=" ")
        posteriors = posteriors.append(p.unstack())

print posteriors.head()
print posteriors.size
plt.hist(posteriors, bins=100)
plt.savefig("../plots/posterior_histograms/main.png")
plt.close()

plt.hist (posteriors [(posteriors < 0.99) & (posteriors > 0.01)], bins = 100)
plt.savefig("../plots/posterior_histograms/subhist.png")
plt.close()

plt.hist (posteriors [(posteriors < 0.9) & (posteriors > 0.1)], bins = 100)
plt.savefig("../plots/posterior_histograms/subsub.png")
plt.close()
