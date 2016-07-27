import pandas as pd
from numpy import interp
import os

# os.chdir("/projects/ingo/local_ancestry/viya_tmp/scripts/")
os.chdir("/Volumes/Greenland/local_ancestry/viya_tmp/scripts/")
chrs = range(1, 23)


# make sure cols 0,1,2 are identical between adm,inuit,ceu
for chr in chrs:
    print chr
    phased_vcf_path_adm = "../intermediate_data/phased/{}_chr{}.vcf.gz".format("adm", chr)
    phased_vcf_path_inuit = "../intermediate_data/phased/{}_chr{}.vcf.gz".format("inuit", chr)
    phased_vcf_path_ceu = "../intermediate_data/phased/{}_chr{}.vcf.gz".format("ceu", chr)
    genetic_map_path = "../raw_data/CHB/CHB-{}-final.txt.gz".format(chr)

    phased_vcf_adm = pd.read_table(phased_vcf_path_adm, comment="#", header=None)
    phased_vcf_inuit = pd.read_table(phased_vcf_path_inuit, comment="#", header=None)
    phased_vcf_ceu = pd.read_table(phased_vcf_path_ceu, comment="#", header=None)

    # Make sure all the rsIDs match
    print "asserting"
    print "vcf_adm size {}".format(phased_vcf_adm[2].size)
    print "vcf_inuit size {}".format(phased_vcf_inuit[2].size)
    print "vcf_ceu size {}".format(phased_vcf_ceu[2].size)
    assert(
        sum(phased_vcf_adm[2] != phased_vcf_inuit[2]) == 0)
    assert(
        sum(phased_vcf_adm[2] != phased_vcf_ceu[2]) == 0)

    adm_alleles = phased_vcf_adm.iloc[:, 9:]
    inuit_alleles = phased_vcf_inuit.iloc[:, 9:]
    ceu_alleles = phased_vcf_ceu.iloc[:, 9:]
    catted = pd.concat([adm_alleles, inuit_alleles, ceu_alleles], axis=1)
    f = open("../intermediate_data/rfmix_in/alleles_chr{}.txt".format(chr), 'w')
    for r in catted.iterrows():
        f.write("".join(r[1]).replace("|", "") + "\n")
    #    break
    f.close()

    genetic_map = pd.read_table(genetic_map_path)
    bim = pd.read_table("../intermediate_data/adm.bim", header=None)
    bim = bim[bim[0] == chr]
    # we have already checked to see that all the rsIDs are identical
    non_filtered_snps = bim[1].isin(phased_vcf_adm[2])
    bim_bool = bim[non_filtered_snps]
    # make sure RSIDs are in the correct order
    assert(sum(bim_bool[1] != phased_vcf_adm[2]) == 0)  # crashhhhhh
    genetic_dist = interp(bim[3], genetic_map["Position(bp)"], genetic_map["Map(cM)"])
    genetic_dist = ["%.15f" % x for x in genetic_dist]
    f = open("../intermediate_data/rfmix_in/snp_locations_chr{}.txt".format(chr), 'w')
    f.write("\n".join(genetic_dist))
    f.close()


f = open("../intermediate_data/rfmix_in/classes.txt".format(chr), 'w')
classes = '0' * (adm_alleles.shape[1] * 2) + \
    '1' * (inuit_alleles.shape[1] * 2) + \
    '2' * (ceu_alleles.shape[1] * 2)
f.write(classes)
f.close()
