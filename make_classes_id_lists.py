import pandas as pd
import os

qs = pd.read_table("../raw_data/qc_ceu_plus_auto_filt.2.Q_1", header = None, sep=" ")
fam = pd.read_table("../raw_data/qc_ceu_plus_auto_filt.fam", header = None, sep = " ")
admixture = pd.concat([qs.loc[:,1], fam.loc[:,0:1]], axis = 1)
admixture.columns = ["EU_admixture", "FID", "IID"]
CEU = admixture[admixture["EU_admixture"] > 0.99]
inuit = admixture[admixture["EU_admixture"] < 0.001]
admixed = admixture[(admixture["EU_admixture"] <=0.99) & (admixture["EU_admixture"]>=0.001)]

admixture.to_csv('../intermediate_data/EU_admixture_fid_iid.txt', sep=" ", index = False)
CEU[["FID","IID"]].to_csv('../intermediate_data/ceu_id_list.txt', sep=" ", index = False)
admixed[["FID","IID"]].to_csv('../intermediate_data/adm_id_list.txt', sep=" ", index = False)
inuit[["FID","IID"]].to_csv('../intermediate_data/inuit_id_list.txt', sep=" ", index = False)
