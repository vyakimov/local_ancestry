import sys
import pandas as pd
import numpy as np
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import linecache

ind_number = int(sys.argv[1])
ingo_ID = linecache.getline("../intermediate_data/adm.fam", ind_number).strip().split()[0]
# make blank plot
# 1388 people in total
data_path = "../intermediate_data/"

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-5, 255)
ax.set_ylim(23, 0)
plt.xlabel("Genetic Position (cM)")
plt.ylabel("Chromosome")
plt.title(ingo_ID)
chromosomes = range(1, 23)
plt.yticks(chromosomes)
# lengths of chr1:22 in cM
chr_end = [247.64,
           234.0,
           212.15,
           192.81,
           185.71,
           176.42,
           166.68,
           152.72,
           150.90,
           157.58,
           146.13,
           155.35,
           114.01,
           106.71,
           110.62,
           119.48,
           116.02,
           110.78,
           100.30,
           97.62,
           52.80,
           59.38]

curviness = 1.5
for c in zip(chromosomes, chr_end):
    chromosome = c[0]
    chr_end = c[1]

    verts = [
        (0, chromosome - 0.45),
        (curviness, chromosome),
        (0, chromosome + 0.45),
        (chr_end, chromosome + 0.45),
        (chr_end - curviness, chromosome),
        (chr_end, chromosome - 0.45),
        (0, 0)
    ]

    codes = [Path.MOVETO,
             Path.CURVE3,
             Path.CURVE3,
             Path.LINETO,
             Path.CURVE3,
             Path.CURVE3,
             Path.CLOSEPOLY,
             ]

    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='#65655E', lw=2)  # grainte gray
    ax.add_patch(patch)
legend_inuit = patches.Patch(color="#65655E", label="Inuit")
legend_ceu = patches.Patch(color="#7D80DA", label="CEU")
legend_undef = patches.Patch(color="#C6AFB1", label="Undetermined")
plt.legend(handles=[legend_inuit, legend_ceu, legend_undef], loc="lower right")


# paint a single chromosome
def paint_chromosome(chromosome, hap, ancestry_begin_end):
    "we assume the whole thing is inuit, and plot CEU and undetermined on top"

    assert ((hap == -1) | (hap == 1))

    for element in ancestry_begin_end:
        ancestry = element[0]
        begin_index = element[1][0]
        end_index = element[1][1]
        if begin_index == 0:
            begin = 0
        else:
            begin = float(
                linecache.getline("{}rfmix_in/snp_locations_chr{}.txt".format(data_path, chromosome),
                                  begin_index).strip())
        if end_index == 0:
            end = 0
        else:
            end = float(
                linecache.getline("{}rfmix_in/snp_locations_chr{}.txt".format(data_path, chromosome),
                                  end_index).strip())

        if ancestry == 'ceu':
            color = "#7D80DA"  # vista blue
        elif ancestry == 'bad':
            color = "#C6AFB1"  # silver pink
        elif ancestry == 'inuit':  # everything is inuit by default
            continue
        else:
            print "unexpected ancestry"
            raise

        verts = [(begin, chromosome),
                 (end, chromosome),
                 (end, chromosome - 0.45 * hap),
                 (begin, chromosome - 0.45 * hap),
                 (0, 0)]
        codes = [Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.CLOSEPOLY]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, lw=1)
        ax.add_patch(patch)
    return


# extract painting coordinates
# 1 = inuit, #2 = ceu
inuit_threshold = 0.1
ceu_threshold = 0.9

a_person = pd.DataFrame(index=np.arange(51372), columns=[
    "haplo1_inuit", "haplo1_ceu", "haplo2_inuit", "haplo2_ceu"])


def lazy(file):
    for line in file:
        yield line

chromosomes = xrange(1, 23)

for chromosome in chromosomes:
    print "doing {} chromosome {}".format(ingo_ID, chromosome)
    fwbck = "{}rfmix_out/chr{}.3.ForwardBackward.txt".format(data_path, chromosome)

    f = open(fwbck, 'r')
    generator = lazy(f)
    # fwdbackward has four fields per individual. Two haplotypes, with two ancestries per haplotype
    # every fourth column is a new individual

    # fill in with tuples, indicating start and end of CEU ancestry
    # (by default we assume ancestry is inuit)
    inuit_index_hap1 = []
    inuit_index_hap2 = []

    index, start_hap_1, start_hap_2 = 0, 0, 0
    flag1, flag2 = "empty", "empty"  # inuit, ceu, or bad

    # for line in file
    for i in generator:
        line = map(float, i.split()[(ind_number * 4 - 4): ind_number * 4])

        if (line[1] < inuit_threshold) & (flag1 is not "inuit"):
            # print "hap1 {}, getting inuit (was {})".format(index, flag1)
            if flag1 is not "empty":
                inuit_index_hap1.append((flag1, (start_hap_1, index)))
            start_hap_1 = index
            flag1 = "inuit"

        if (line[1] >= ceu_threshold) & (flag1 is not "ceu"):
            # print "hap1 {}, getting ceu (was {})".format(index, flag1)
            if flag1 is not "empty":
                inuit_index_hap1.append((flag1, (start_hap_1, index)))
            start_hap_1 = index
            flag1 = "ceu"

        if ((line[1] <= ceu_threshold) & (line[1] > inuit_threshold) & (flag1 is not "bad")):
            # print "hap1 {}, getting bad :( (was {})".format(index, flag1)
            if flag1 is not "empty":
                inuit_index_hap1.append((flag1, (start_hap_1, index)))
            start_hap_1 = index
            flag1 = "bad"

        if (line[3] < inuit_threshold) & (flag2 is not "inuit"):
            # print "hap2 {}, getting inuit :) (was {})".format(index, flag2)
            if flag2 is not "empty":
                inuit_index_hap2.append((flag2, (start_hap_2, index)))
            start_hap_2 = index
            flag2 = "inuit"

        if (line[3] >= ceu_threshold) & (flag2 is not "ceu"):
            # print "hap2 {}, getting ceu (was {})".format(index, flag2)
            if flag2 is not "empty":
                inuit_index_hap2.append((flag2, (start_hap_2, index)))
            start_hap_2 = index
            flag2 = "ceu"

        if ((line[3] <= ceu_threshold) & (line[3] > inuit_threshold) & (flag2 is not "bad")):
            # print "hap2 {}, getting bad :( (was {})".format(index, flag2)
            if flag2 is not "empty":
                inuit_index_hap2.append((flag2, (start_hap_2, index)))
            start_hap_2 = index
            flag2 = "bad"

        index = index + 1

    inuit_index_hap1.append((flag1, (start_hap_1, index)))
    inuit_index_hap2.append((flag2, (start_hap_2, index)))

    # print inuit_index_hap1
    # print inuit_index_hap2

    paint_chromosome(chromosome, -1, inuit_index_hap1)
    paint_chromosome(chromosome, 1, inuit_index_hap2)

    f.close()

plt.savefig("../plots/{}_local_ancestry.png".format(ingo_ID))
plt.close()
