rm(list=ls())
require(preprocessCore)
setwd("/projects/ingo/local_ancestry/viya_tmp/scripts")
options(stringsAsFactors = FALSE) 
require(data.table)

phenotype_names = commandArgs(trailingOnly=TRUE)[1]
# phenotype_names = "UnSat"
# print(phenotype_names)
# 

phenotypes = as.data.table(read.table("/data/INGO/NMR_2015sep09/results.txt", as.is=T))
header = as.character(read.table("/data/INGO/NMR_2015sep09/headers_clean.txt", as.is=T))
colnames(phenotypes) = c("INGOID", as.character(header))
ids = as.data.table(as.character(read.table("../intermediate_data/gemma_in/IDs")$V1))
flagged_ingos = as.character(read.table("/data/INGO/NMR_2015sep09/flagged_ingos.txt")$V1)
setkey(phenotypes, "INGOID")

phenotypes = phenotypes[ids]

distribution = phenotypes[,get(phenotype_names)]

n_ingo = length(distribution)
target = qnorm(seq(1/n_ingo, (n_ingo-1) / n_ingo, 1/n_ingo))
normalized_distribution = as.data.frame(cbind(ids, normalize.quantiles.use.target(as.matrix(distribution), target ) ))
normalized_distribution[normalized_distribution[,1] %in% flagged_ingos,][,2] = NA

write.table(normalized_distribution[,-1], paste0("../intermediate_data/gemma_in/normed_phenotypes/", phenotype_names), quote=F, sep=" ", row.names=F,col.names=F)
#write.table(phenotype_names, "../intermediate_data/gemma_in/normed_phenotypes/names", quote=F, sep=" ", row.names=F,col.names=F)
