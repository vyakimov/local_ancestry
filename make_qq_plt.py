import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.stats
EXPECTED_MEDIAN = scipy.stats.chi2.ppf(0.5, 1)

gemma_out_path="../interm_diate_data/gemma_out/UnSat/UnSat.assoc.txt"
# outpath = "." 
# excl_chr = 11

gemma_out_path = sys.argv[1]
try:
	outpath = sys.argv[2]
except:
	pheno_name = gemma_out_path.split("/")[4].split(".")[0]
	outpath = "../intermediate_data/gemma_out/{}/".format(pheno_name)

try:
	excl_chr = int(sys.argv[3])
except:
	excl_chr = None


pvals = pd.read_table(gemma_out_path)["p_wald"].convert_objects(convert_numeric=True)
if excl_chr is not None:
    chr_col = pd.read_table(gemma_out_path)["chr"]
    excl_index = chr_col[chr_col == int(excl_chr)].index
    pvals[excl_index] = None
    pvals = pvals.dropna()

stats = scipy.stats.chi2.ppf(1 - pvals, 1)



pvals.sort()
pvals = pvals[pvals.notnull()]
lobs = -np.log10(pvals)
expected = pd.Series(np.arange(1.0, len(lobs) + 1))
lexp = -np.log10(expected / (len(expected) + 1))
max_val = max(max(lobs), max(lexp))
inf_factor = round(np.median(stats) / EXPECTED_MEDIAN, 5)
plt.plot([0, max_val], [0, max_val], linestyle='-', linewidth=1)
plt.plot(lexp, lobs, 'ro')
plt.title("lambda={}".format(inf_factor))
plt.xlabel("expected")
plt.ylabel("observed")
print "saving to {}".format(outpath)
plt.savefig(outpath)
plt.close()
