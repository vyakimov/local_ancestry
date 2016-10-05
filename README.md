#Local Ancestry Phasing

* `make_classes_id_lists.py` will create four files: 
	* A file with FIDs IIDs and CEU admixture proportions
	* Three files with IDs for CEU / Inuit / Admixed individuals
* `split_plink.sh` will:
	* remove duplicate SNPs
	* split genotypes based into three (CEU/Inuit/Admixed)
	* create VCF files for beagle
* `fix_vcf.py` will fix VCF files to make Beagle happier by:
	* removing I and D from reference allele fields
	* replaceing . to N in alternate allele fields
* `phase.sh` will run Beagle 
* `make_rfmix_input.py` will create the necessary files for RFMix by taking Beagle output 
* `run_rfmix.sh` will run RFMix 
* `plot_local_ancestry.py` will take RFMix output and generate local ancestry plots 
* `convert_fwbck_to_gemma.py` will take RFMix output (the forwardback files), and convert them to input for GEMMA. Its output is a snp file and a genotype file, both required by GEMMA
* `histograms_la_posteriors.py` will take forward backwards files output from RFMix, and make a histogram from them (the idea being to check the distribution of posterior probabilities, and make sure it looks more or less bimodal)
* `make_gemma_phenotypes.R` will take a raw phenotype, quantile normalize it, and output it in a format which GEMMA is happy with. It only uses a single phenotype at a time
* `make_kinship.sh` wlil make a kinship matrix using gemma using admixed and fully inuit individuals. We filter with --maf 0.05 --geno 0.01 and remove duplicates prior to making the kinship matrix
*  `make_qq_plt.py` will take gemma output (all chromosomes concatinated), and output a qqplot
* `manhattan-plot.py` wil ltake gemma output (all chromosomes concatinated), and output a manhattan plot
* `run_gemma.sh` is a wrapper for running gemma, with a kinship matrix, a covar file, a phenotypes fils and a snps+genotypes file 
* `validate_local_ancestry.py` will make sure the sum of local ancestry matches the global ancestry estimate

(Note, RFMix was partly run on the computerome. The same parameters were used as run_rfmix.sh)