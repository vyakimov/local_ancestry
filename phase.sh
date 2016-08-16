for class in adm ceu inuit 
do
	java -Xmx40g -jar ~/bin/beagle.05Jul16.587.jar gt=../intermediate_data/beagle_in_fixed_${class}.vcf out=../intermediate_data/phased/${class} &> ${class}.log
	seq 1 22 | parallel "vcftools --recode --gzvcf ${class}.vcf.gz --chr {} --out ${class}_chr{}"
done
rename .recode. . *.recode.vcf
echo "gzipping"
ls *vcf | parallel gzip {}
