from __future__ import print_function
from numpy import mean, repeat

# Here we take RFMix output, compress all the windows, and output one ancestry per window

chromosomes = range(1, 23)
data_path = "../intermediate_data/"

# FWDBCK file is structured (each row is a snp)
# ind1_hap1_anc1 ind1_hap1_anc2 ind1_hap2_anc1 ind1_hap2_anc2 ind2_hap1_anc1 ...

# there are four columns per individual

# count numbeer of pure inuit individuals
with open("{}inuit.fam".format(data_path)) as f:
    for i, l in enumerate(f):
        pass
    inuit_count = i + 1

for chromosome in chromosomes:
    snpfile = open("{}gemma_in/chr{}_ancestry.snps".format(data_path, chromosome), 'w')
    genofile = open("{}gemma_in/chr{}_ancestry".format(data_path, chromosome), 'w')
    fwdbck = "{}rfmix_out/chr{}.3.ForwardBackward.txt".format(data_path, chromosome)
#    brks = "{}/rfmix_out/chr{}_breaks.txt".format(data_path, chromosome)
    snpPos = 0
    previous_line = -1.0
    breaks = []
    with open(fwdbck, 'r') as f:
        for line in f:
            snpPos = snpPos + 1
            spltline = line.strip().split(" ")
            # each element is a column, each fourth element is a new person

            summed_line = sum([float(x) for x in spltline])
            if (summed_line == previous_line):
                continue
            else:
                breaks.append(snpPos)
                ancestry_vector = [int(round(float(x))) for x in spltline]
                # since ancestry1 + ancestry2 == 1, we can throw out every second column
                ancestry_vector = ancestry_vector[::2]
                # take mean of hap1 and hap2
                mean_ancestry = [str(mean(x) + 1) for x in zip(ancestry_vector[::2], ancestry_vector[1::2])]
                # 2 is inuit, 1 is CEU
                mean_ancestry += repeat("2.0", inuit_count)
                ancestry_vector = ",".join(mean_ancestry)
                print("c{}p{},T,G,{}".format(chromosome, snpPos, ancestry_vector), file=genofile)
                print("c{}p{},{},{}".format(chromosome, snpPos, snpPos, chromosome), file=snpfile)

                previous_line = summed_line

    breaks = [str(x) for x in breaks]
snpfile.close()
genofile.close()
