name=$1 ##name as header in /data/INGO/NMR_2015sep09/headers_clean.txt
headers="/data/INGO/NMR_2015sep09/headers_clean_column.txt"
function werk(){
	if [ -z $1 ]; then
		echo "needs a pheno name"
	else
		name="$1"
		ptgo="../intermediate_data/gemma_out/${name}/"
		echo working on $name
		Rscript make_gemma_phenotypes.R ${name}
		seq 1 22 | parallel ./run_gemma.sh {} ${name}
		head -1 ${ptgo}chr1.assoc.txt > ${ptgo}${name}.assoc.txt
		for i in `seq 1 22` 
		do
			tail -n +2 -q ${ptgo}chr${i}.assoc.txt >> ${ptgo}${name}.assoc.txt
		done
		# rm ${ptgo}chr*assoc*
		python manhattan-plot.py --image ../plots/manhattan/${name}.manhattan.pdf ${ptgo}${name}.assoc.txt
		python make_qq_plt.py ${ptgo}${name}.assoc.txt ../plots/qq/${name}.qq.png
	fi
}

echo working on $name
if [ $name = "allofthephenos" ]; then
	while IFS=$'\n\r \t' read -r line; do
		werk "$line"
	done < $headers
else
	werk $name
fi
