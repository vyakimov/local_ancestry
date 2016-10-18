#!/usr/bin/bash
CHR=$1
PHENO_NAME=$2 #GEMMA WILL ALWAYS OUTPUT IN ./output AND WILL JUST CONCATINATE OUT_DIR TO ./output AND THEN CRASH IF YOU GIVE IT E.G. A RELATIVE PATH.
GEMMA_IN_DIR=../intermediate_data/gemma_in/
# 

GENOTYPES=${GEMMA_IN_DIR}chr${CHR}_ancestry
SNPS=${GEMMA_IN_DIR}chr${CHR}_ancestry.snps
PHENOTYPES=${GEMMA_IN_DIR}normed_phenotypes/${PHENO_NAME}
COVAR=${GEMMA_IN_DIR}age_sex_bmi_covar.txt
KINSHIP=${GEMMA_IN_DIR}kinship_w_pruning.sXX.txt
OUTPUT="chr${CHR}"

gemma -g $GENOTYPES -p $PHENOTYPES -a $SNPS -k $KINSHIP -lmm 1 -km 1 -c $COVAR -maf 0.001 -o $OUTPUT

mkdir -p ../intermediate_data/gemma_out/${PHENO_NAME}
mv ./output/${OUTPUT}* ../intermediate_data/gemma_out/${PHENO_NAME}/
