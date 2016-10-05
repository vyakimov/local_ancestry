#!/usr/bin/bash
CHR=$1

GEMMA_IN_DIR=../intermediate_data/gemma_in/
# GEMMA_OUT_DIR=../intermediate_data/gemma_out/ #GEMMA WILL ALWAYS OUTPUT IN ./output AND WILL JUST CONCATINATE OUT_DIR TO ./output AND THEN CRASH IF YOU GIVE IT E.G. A RELATIVE PATH

GENOTYPES=${GEMMA_IN_DIR}chr${CHR}_ancestry
SNPS=${GEMMA_IN_DIR}chr${CHR}_ancestry.snps
PHENOTYPES=${GEMMA_IN_DIR}normed_phenotypes
COVAR=${GEMMA_IN_DIR}age_sex_bmi_covar.txt
KINSHIP=${GEMMA_IN_DIR}kinship_wo_chr11.sXX.txt
OUTPUT=chr${CHR}

gemma -g $GENOTYPES -p $PHENOTYPES -a $SNPS -k $KINSHIP -lmm 1 -km 1 -c $COVAR -maf 0.001 -o $OUTPUT
mv ./output/${OUTPUT}* ${GEMMA_OUT_DIR}
rmdir ./output
