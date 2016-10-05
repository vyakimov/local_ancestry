cd ../intermediate_data/
mkdir plink_out
cat adm_id_list.txt inuit_id_list.txt > adm_inuit_id_list.txt
plink --bfile ../raw_data/qc_ceu_plus_auto_filt --keep adm_inuit_id_list.txt --chr 1-10,12-22 --make-bed --out plink_out/set1
plink --bfile plink_out/set1 --maf 0.05 --geno 0.01 --make-bed --out plink_out/set2
plink --bfile plink_out/set2 --list-duplicate-vars --out plink_out/dupvars
plink --bfile plink_out/set2 --exclude plink_out/dupvars.dupvar --make-bed --out plink_out/set3

rm plink_out/set1* plink_out/set2* plink_out/dupvars.*

gemma -bfile plink_out/set3 -gk 2 -o kinship_wo_chr11
mv output/* ../intermediate_data/gemma_in/
rmdir output
rm -rf plink_out
