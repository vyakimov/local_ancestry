BEDBIMFAM=.bed .bim .fam
BASENAME_GENOTYPES=../raw_data/qc_ceu_plus_auto_filt
ADMIX_PROPORTIONS=../raw_data/qc_ceu_plus_auto_filt.2.Q_1
ADMIX_PROPORTIONS_FAM=../raw_data/qc_ceu_plus_auto_filt.fam
EU_ADMIXTURE=../intermediate_data/EU_admixture_fid_iid.txt
ID_LISTS=../intermediate_data/*_id_list.txt
DUPLICATES=../intermediate_data/qc_ceu_plus_auto_filt.dupvar
GENOTYPES=$(addprefix $(BASENAME_GENOTYPES), $(BEDBIMFAM))
BASENAME_SPLIT_GENOTYPES = ../intermediate_data/adm ../intermediate_data/ceu ../intermediate_data/inuit
BASENAME_SPLIT_GENOTYPES_BIMBAMFAM = $(foreach type, $(BASENAME_SPLIT_GENOTYPES), $(addprefix $(type), $(BEDBIMFAM))) #3*3 of ceu ADM inuit * bed bim fam
VCFs = $(addprefix ../intermediate_data/beagle_in_, adm.vcf ceu.vcf inuit.vcf)

.PHONY: all
all: $(VCFs)

## recode to VCFs so that beagle is happy
$(VCFs) : $(BASENAME_SPLIT_GENOTYPES_BIMBAMFAM)
	plink --bfile $(subst beagle_in_,,$(basename $@))\
		  --recode vcf --keep-allele-order\
		  --out $(basename $@)

## Split genotypes into CEU, admixed, Inuit
$(BASENAME_SPLIT_GENOTYPES_BIMBAMFAM) : $(ID_LISTS) $(DUPLICATES) $(GENOTYPES)
	plink --bfile $(BASENAME_GENOTYPES)\
	  --keep $(addsuffix _id_list.txt, $(basename $@))\
	  --make-bed --keep-allele-order\
	  --exclude $(DUPLICATES)\
	  --out $(basename $@)

## mark duplicates 
$(DUPLICATES) : $(GENOTYPES)
	plink --bfile $(BASENAME_GENOTYPES) --list-duplicate-vars suppress-first --out $(basename $(DUPLICATES))

## create lists of IDs of CEU, Inuit, and admixed individuals
$(EU_ADMIXTURE) $(ID_LISTS) : $(ADMIX_PROPORTIONS) $(ADMIX_PROPORTIONS_FAM)
	python make_classes_id_lists.py