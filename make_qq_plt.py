import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.stats
EXPECTED_MEDIAN = scipy.stats.chi2.ppf(0.5, 1)

gemma_out_path = sys.argv[1]
outpath = sys.argv[2]

pvals = pd.read_table(gemma_out_path)["p_wald"].convert_objects(convert_numeric=True)
stats = scipy.stats.chi2.ppf(1-pvals, 1)
inf_factor = round( np.median(stats) / EXPECTED_MEDIAN, 5 )

pvals.sort()
pvals = pvals[pvals.notnull()]
lobs = -np.log10(pvals)
expected = pd.Series(np.arange(1.0, len(lobs) + 1))
lexp = -np.log10(expected / (len(expected) + 1))
max_val = max(max(lobs), max(lexp))
plt.plot([0, max_val], [0, max_val], linestyle='-', linewidth=1)
plt.plot(lexp, lobs, 'ro')
plt.title("lambda={}".format(inf_factor))
plt.xlabel("expected")
plt.ylabel("observed")
plt.savefig(outpath)
plt.close()
