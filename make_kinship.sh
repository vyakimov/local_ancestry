cd ../intermediate_data/
mkdir plink_out
cat adm_id_list.txt inuit_id_list.txt > adm_inuit_id_list.txt
# plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep adm_inuit_id_list.txt --chr 1-10,12-22 --make-bed --out plink_out/set1

## filter on admixed and pure inuit individuals 
plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep adm_inuit_id_list.txt --indiv-sort f adm_inuit_id_list.txt --make-bed --out plink_out/set1
plink --bfile plink_out/set1 --maf 0.05 --geno 0.01 --make-bed --out plink_out/set2
## remove duplicates
plink --bfile plink_out/set2 --list-duplicate-vars --out plink_out/dupvars
plink --bfile plink_out/set2 --exclude plink_out/dupvars.dupvar --make-bed --out plink_out/set3
## LD prune 
plink --bfile plink_out/set3 --indep 50 5 1.5 --out plink_out/set4
plink --bfile plink_out/set3 --extract plink_out/set4.prune.in --make-bed --out plink_out/set4

rm plink_out/set1* plink_out/set2* plink_out/set3* plink_out/dupvars.*

## -gk 2 calcualates standardized relationship matrix [1 calculates centered relatedness matrix]

gemma -bfile plink_out/set4 -gk 2 -o kinship_w_pruning
mv output/* ../intermediate_data/gemma_in/
rmdir output
## rm -rf plink_out
