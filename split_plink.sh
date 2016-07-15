# Removing duplicate SNPs
plink --bfile ../raw_data/qc_ceu_plus_auto_filt --list-duplicate-vars suppress-first --out ../intermediate_data/qc_ceu_plus_auto_filt


# Splitting data using plink
plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep ../intermediate_data/adm_id_list.txt --make-bed --keep-allele-order --exclude ../intermediate_data/qc_ceu_plus_auto_filt.dupvar --out ../intermediate_data/adm

plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep ../intermediate_data/ceu_id_list.txt --make-bed --keep-allele-order --exclude ../intermediate_data/qc_ceu_plus_auto_filt.dupvar --out ../intermediate_data/ceu

plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep ../intermediate_data/inuit_id_list.txt --make-bed --keep-allele-order --exclude ../intermediate_data/qc_ceu_plus_auto_filt.dupvar --out ../intermediate_data/inuit

#convert to beagle4-friendly VCF
for class in inuit ceu adm
do
plink --bfile ../intermediate_data/$class --recode vcf --keep-allele-order --out ../intermediate_data/beagle_in_$class
done
