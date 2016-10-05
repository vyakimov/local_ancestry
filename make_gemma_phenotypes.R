rm(list=ls())
require(preprocessCore)
setwd("/projects/ingo/local_ancestry/viya_tmp/scripts")

phenotype_names = commandArgs(trailingOnly=TRUE)[1]

# print(phenotype_names)
# 

phenotypes = read.table("/data/INGO/NMR_2015sep09/results.txt")
header = as.character(read.table("/data/INGO/NMR_2015sep09/headers.txt", as.is=T))
colnames(phenotypes) = c("INGOID", as.character(header))
ids = as.character(read.table("../intermediate_data/gemma_in/IDs")$V1)
flagged_ingos = as.character(read.table("/data/INGO/NMR_2015sep09/flagged_ingos.txt")$V1)



phenotypes = phenotypes[as.character(phenotypes$INGOID) %in% ids,]
#phenotypes = phenotypes[(as.character(phenotypes$INGOID) %in% flagged_ingos)]
distribution = phenotypes[phenotype_names]



n_ingo = nrow(distribution)
target = qnorm(seq(1/n_ingo, (n_ingo-1) / n_ingo, 1/n_ingo))
normalized_distribution = cbind(ids, normalize.quantiles.use.target(as.matrix(distribution), target ) )
normalized_distribution[normalized_distribution[,1] %in% flagged_ingos,][,2] = NA

write.table(normalized_distribution[,-1], paste0("../intermediate_data/gemma_in/normed_phenotypes/", phenotype_names), quote=F, sep=" ", row.names=F,col.names=F)
write.table(phenotype_names, "../intermediate_data/gemma_in/normed_phenotypes/names", quote=F, sep=" ", row.names=F,col.names=F)
