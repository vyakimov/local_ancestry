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


(Note, RFMix was partly run on the computerome. The same parameters were used as run_rfmix.sh)
