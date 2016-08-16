OPTS="--forward-backward -e 3 -n 5 PopPhased"
RFMIX=/home/ssi.ad/viya/bin/RFMix_v1.5.4

for i in {1..22}
do
	CHR=${i}
	ALLELES=/projects/ingo/local_ancestry/viya_tmp/intermediate_data/rfmix_in/alleles_chr${CHR}.txt
	CLASSES=/projects/ingo/local_ancestry/viya_tmp/intermediate_data/rfmix_in/classes.txt
	LOCS=/projects/ingo/local_ancestry/viya_tmp/intermediate_data/rfmix_in/snp_locations_chr${CHR}.txt
	OUT=/projects/ingo/local_ancestry/viya_tmp/intermediate_data/rfmix_out/chr${CHR}

	cd ${RFMIX}
	python RunRFMix.py ${OPTS} ${ALLELES} ${CLASSES} ${LOCS} -o ${OUT}
done

# python ../../painting_haplotypes/RFMix_v1.5.4/RunRFMix.py --forward-backward -e 3 PopPhased ../intermediate_data/rfmix_in/alleles_chr11.txt ../intermediate_data/rfmix_in/classes.txt ../intermediate_data/rfmix_in/snp_locations_chr11.txt -o ../intermediate_data/rfmix_out/chr1

## works: 
#python RunRFMix.py --forward-backward -e 3 PopPhased ../../painting_haplotypes/RFmix_in/alleles_chr_11.txt ../../painting_haplotypes/RFmix_in/classes.txt ../../painting_haplotypes/RFmix_in/snp_locations_adm.bim -o ../intermediate_data/rfmix_out/chr1
