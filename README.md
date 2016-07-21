#Local Ancestry Phasing

* make_classes_id_lists.py will create four files: 
	* A file with FIDs IIDs and CEU admixture proportions
	* Three files with IDs for CEU / Inuit / Admixed individuals
* split_plink.sh will:
	* remove duplicate SNPs
	* split genotypes based into three (CEU/Inuit/Admixed)
	* create VCF files for beagle
* fix_vcf.py will fix VCF files to make Beagle happier by:
	* removing I and D from reference allele fields
	* replaceing . to N in alternate allele fields

