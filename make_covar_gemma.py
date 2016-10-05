import pandas as pd
from numpy import timedelta64, repeat

adm_ingo_ids = pd.read_table("../intermediate_data/adm.fam", sep=" ", header=None)[0].append(
    pd.read_table("../intermediate_data/inuit.fam", sep=" ", header=None)[0])

hgt_wgt_loc = pd.read_table("../raw_data/INGO_7towns_hgt_wgt_bp_2015okt15_corrected.txt", sep=" ")
gender_DOB = pd.read_table("../raw_data/ingo_person_list.txt", sep=" ",
                           index_col=False, usecols=["id", "koen", "fdato"])
gender_DOB["fdato"] = (pd.datetime(2013, 7, 1) - pd.to_datetime(gender_DOB["fdato"])) / timedelta64(1, 'Y')
gender_DOB["koen"] = gender_DOB["koen"].replace(["K", "M"], [1, 0])
gender_DOB.index = gender_DOB["id"]


hgt_wgt_loc["bmi"] = hgt_wgt_loc["wgt"] / (hgt_wgt_loc["hgt"] / 100) ** 2
hgt_wgt_loc.index = hgt_wgt_loc["ID"]

covariate_dt = pd.DataFrame(index=adm_ingo_ids)

covariate_dt["intercept"] = repeat(1, len(covariate_dt))
covariate_dt = pd.merge(covariate_dt, gender_DOB[["koen", "fdato"]],
                        how='left', left_index=True, right_index=True)

covariate_dt = pd.merge(covariate_dt, hgt_wgt_loc[["bmi"]], how='left', left_index=True, right_index=True)
covariate_dt.columns = ["intercept", "sex", "age", "bmi"]

covariate_dt.to_csv("../intermediate_data/gemma_in/age_sex_bmi_covar.txt", sep=" ", header=False, index=False, na_rep="NA")
adm_ingo_ids.to_csv("../intermediate_data/gemma_in/IDs",header=False,index=False,na_rep="NA")