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
VCFs = adm.vcf ceu.vcf inuit.vcf
CHROMOSOMES = 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22
TYPES = adm ceu inuit
ADM_BEAGLE_OUT = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/phased/adm_chr${chr}.vcf.gz)
INUIT_BEAGLE_OUT = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/phased/inuit_chr${chr}.vcf.gz)
CEU_BEAGLE_OUT = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_in/ceu_chr${chr}.vcf.gz)
RFMIX_IN_ALLELES = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_in/alleles_chr${chr}.txt)
RFMIX_IN_SNP_LOCATIONS = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_in/snp_locations_chr${chr}.txt)
RFMIX_IN_CLASSES = ../intermediate_data/rfmix_in/classes.txt
GENETIC_MAP = $(foreach chr, ${CHROMOSOMES}, ../raw_data/CHB/CHB-${chr}-final.txt.gz)
RFMIX_OUT_FWDBCK = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_out/chr${chr}.3.ForwardBackward.txt)
RFMIX_OUT_VIT = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_out/chr${chr}.3.Viterbi.txt)
RFMIX_OUT_REPHASED = $(foreach chr, ${CHROMOSOMES}, ../intermediate_data/rfmix_out/chr${chr}.allelesRephased3.txt)

.PHONY: all
all: RFMIX_OUT_FWDBCK RFMIX_OUT_VIT RFMIX_OUT_REPHASED

## run RFMix 
RFMIX_OUT_FWDBCK RFMIX_OUT_VIT RFMIX_OUT_REPHASED : RFMIX_IN_ALLELES RFMIX_IN_SNP_LOCATIONS RFMIX_IN_CLASSES
	./run_rfmix.sh

## make files for RFMix
RFMIX_IN_ALLELES RFMIX_IN_SNP_LOCATIONS RFMIX_IN_CLASSES : ADM_BEAGLE_OUT INUIT_BEAGLE_OUT CEU_BEAGLE_OUT GENETIC_MAP
	python make_rfmix_input.py

## phase using Beagle, split results by chromosome, and GZip them
ADM_BEAGLE_OUT INUIT_BEAGLE_OUT CEU_BEAGLE_OUT : $(addprefix ../intermediate_data/beagle_in_fixed_, $(VCFs))
	./phase.sh 

## edit VCFs to make Beagle happy
$(addprefix ../intermediate_data/beagle_in_fixed_, $(VCFs)) : $(addprefix ../intermediate_data/beagle_in_, $(VCFs))
	python fix_vcfs.py $(subst fixed_,,$@) > $@

## recode to VCFs so that beagle is happy
$(addprefix ../intermediate_data/beagle_in_, $(VCFs)) : $(BASENAME_SPLIT_GENOTYPES_BIMBAMFAM)
	plink --bfile $(subst beagle_in_,,$(basename $@))\
		  --recode vcf-iid --keep-allele-order\
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
