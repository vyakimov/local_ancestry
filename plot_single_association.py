# <codecell>
import pandas as pd
import numpy as np
import linecache
import matplotlib.pyplot as plt
import re
# <markdowncell>
# This script will take gemma input, and do what  gemma does, only manually and naively
# i.e. it won't use complicated mixture models or correct for ancestry
# it will just do a simple linear regression of a single marker (SNP or otherwise)
# and print a p-value and make a plot


# <codecell>
def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


# <codecell>
chromosome = 11
pheno = "UnSat"
pos = 68754889  # beginnign of cpt1a
base_path = "/projects/ingo/local_ancestry/viya_tmp/intermediate_data/gemma_in/"
snp_file = pd.read_table("{}chr{}_ancestry.snps".format(base_path, chromosome), header=None, sep=",")
snp_file.columns = ['name', 'pos', 'chr']
idx = find_nearest(snp_file["pos"], pos)
X = np.array(linecache.getline("chr{}_ancestry".format(chromosome), idx +
                               1).strip().split(",")[3:], dtype=np.float16)  # line idx is 1-based
Y = np.array(pd.read_table("normed_phenotypes/{}".format(pheno), header=None)[0])
assert(X.shape == Y.shape)
a = Y[X == 1]
b = Y[X == 1.5]
c = Y[X == 2]

plt.boxplot([a, b, c])
plt.show()

phenos = pd.read_table("/data/INGO/NMR/NMR.rawResults")
genos = pd.read_table("/projects/ingo/local_ancestry/viya_tmp/raw_data/tmp/plink.recode.geno.txt",
                      skiprows=2, delimiter=",", header=None).transpose()
h = genos.iloc[0]
genos = genos[1:]
genos = genos.rename(columns=h)
genos = genos.set_index("IND")
phenos = phenos.set_index("NAME")
m = genos.join(phenos, how='inner')
uniq = m["rs3019594"].unique()

a = m[m["rs3019594"] == uniq[0]]
a = a["UnsatDeg"]
b = m[m["rs3019594"] == uniq[1]]
b = b["UnsatDeg"]
c = m[m["rs3019594"] == uniq[2]]
c = c["UnsatDeg"]
plt.boxplot([a, b, c])
plt.show()

IDs = pd.read_table("{}../gemma_in/IDs".format(base_path), header=None)
normed_pheno = pd.read_table("{}../gemma_in/normed_phenotypes/UnSat".format(base_path), header=None)
df = pd.concat([IDs, normed_pheno], axis=1)
df.columns = ["IND", "VAL"]
df = df.set_index("IND")
m = genos.join(df, how='inner')
uniq = m["rs3019594"].unique()

a = m[m["rs3019594"] == uniq[0]]
a = a["VAL"]
b = m[m["rs3019594"] == uniq[1]]
b = b["VAL"]
c = m[m["rs3019594"] == uniq[2]]
c = c["VAL"]
plt.boxplot([a, b, c])
plt.show()

geno = pd.read_table("/data/INGO/extra_5_LGC_snps/plink/plink.recode.geno.txt", skiprows=2, delimiter=",")
p = re.compile("(INGO)(\w{2})(\d{4})")
geno.columns.values[1:] = [p.match(x).group(1) + "." + p.match(x).group(3) for x in geno.columns.values[1:]]

# pos = pd.read_table("/data/INGO/extra_5_LGC_snormnps/plink/plink.recode.pos.txt", header=None, sep=" ")
# pos[pos[0]=="rs80356779"]

geno = geno.set_index("IND")
geno = geno.transpose()
geno = geno.join(df, how='inner')

a = geno[geno["rs80356779"] == "AA"]["VAL"]
b = geno[geno["rs80356779"] == "GA"]["VAL"]
c = geno[geno["rs80356779"] == "GG"]["VAL"]
plt.boxplot([a, b, c])
plt.show()




normed_phenos = pd.read_table(
    "/projects/ingo/gemma_imputed_analysis/annotation/NMR/NMR.phenos", header=None, sep=" ")
normed_phenos = normed_phenos.ix[:, 0:232]
normed_phenos_names = pd.read_table(
    "/projects/ingo/gemma_imputed_analysis/annotation/NMR/pheno-names.NMR", sep="|", header=None)
normed_phenos_names[1]
normed_phenos.columns = normed_phenos_names[1]
normed_ids = pd.read_table(
    "/projects/ingo/gemma_imputed_analysis/annotation/INGOs-in-order.txt", header=None)[0]
normed_phenos = normed_phenos.set_index(normed_ids)
npm = normed_phenos.merge(geno, left_index=True, right_index=True)
npm = npm[["UnsatDeg", "VAL"]]

n = 61
m = 75
plt.scatter(npm.dropna()[n:m]["UnsatDeg"], npm.dropna()[n:m]["VAL"])
plt.show()

n = 65
m = 120
plt.scatter(npm.dropna()[n:m]["UnsatDeg"], npm.dropna()[n:m]["VAL"])
plt.show()


# check big snp relative to unnormed genotype
