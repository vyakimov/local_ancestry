#Local Ancestry Phasing

* make_classes_id_lists.py will create four files: 
	* A file with FIDs IIDs and CEU admixture proportions
	* Three files with IDs for CEU / Inuit / Admixed individuals
* split_plink.sh will:
	* remove duplicate SNPs
	* split genotypes based into three (CEU/Inuit/Admixed)
	* create VCF files for beagle
