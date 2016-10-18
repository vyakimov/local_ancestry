name=$1 ##name as header in /data/INGO/NMR_2015sep09/headers.txt
ptgo="../intermediate_data/gemma_out/${name}/"

Rscript make_gemma_phenotypes.R ${name}
seq 1 22 | parallel ./run_gemma.sh {} ${name}
head -1 ${ptgo}chr1.assoc.txt > ${ptgo}${name}.assoc.txt
for i in `seq 1 22` 
do
	tail -n +2 -q ${ptgo}chr${i}.assoc.txt >> ${ptgo}${name}.assoc.txt
done
# rm ${ptgo}chr*assoc*

python manhattan-plot.py --image ${ptgo}${name}.manhattan.png ${ptgo}${name}.assoc.txt
python make_qq_plt.py ${ptgo}${name}.assoc.txt ${ptgo}${name}.qq.png

