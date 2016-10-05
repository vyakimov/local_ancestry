import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# mountpoint = "/Volumes/Greenland/local_ancestry/viya_tmp/"
mountpoint = "/projects/ingo/local_ancestry/viya_tmp/"


global_admixture = pd.read_table(mountpoint + "intermediate_data/EU_admixture_fid_iid.txt", sep=" ")
adm_IDs = pd.read_table(mountpoint + "intermediate_data/adm.fam", names=None, header=None, sep=" ")[1]
print global_admixture.head()
chromosome_admixture = pd.DataFrame(index=adm_IDs, columns=range(1, 23))
adm_global_admixture = global_admixture[global_admixture["FID"].isin(adm_IDs)]


for chromosome in range(1, 23):
    print "doing chromosome {}".format(chromosome)
    local_admixture = pd.read_table(mountpoint + "intermediate_data/rfmix_out/chr{}.3.Viterbi.txt".format(chromosome),
                                    header=None, sep=' ', names=None, engine='c')

    local_admixture = local_admixture.transpose()
    for row in local_admixture.iterrows():
        if row[0] % 2 == 0:
            if row[0] != 0:
                ingo_id = adm_IDs[row[0] / 2 - 1]
                chromosome_admixture[chromosome][ingo_id] = ancestry
            ancestry_one = row[1].mean()
        else:
            ancestry_two = row[1].mean()
            ancestry = (ancestry_two + ancestry_one) / 2
print("data loaded")

local_admixture = chromosome_admixture.mean(axis=1) - 1
global_eu_admixture = adm_global_admixture["EU_admixture"]

local_admixture.index = global_eu_admixture.index
admix_corr = local_admixture.corr(global_eu_admixture)
print "correlation {}".format(admix_corr)

plt.scatter(local_admixture, global_eu_admixture)
plt.plot(np.arange(0, 1, 0.01), np.arange(0, 1, 0.01))
plt.xlabel("local admixture")
plt.ylabel("global admixture")

plt.show()
