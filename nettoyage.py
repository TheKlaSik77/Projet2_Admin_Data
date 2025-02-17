import pandas as pd
import os
import ast
import re

data_path = "./data/job_descriptions.pkl"

#test gaspard

# Charger depuis Pickle si le fichier existe, sinon lire le CSV et le sauvegarder
if os.path.exists(data_path):
    jobs = pd.read_pickle(data_path)
else:
    jobs = pd.read_csv("./data/job_descriptions.csv", index_col=0)
    jobs.to_pickle(data_path)  # Sauvegarde pour la prochaine fois

pd.set_option('display.max_colwidth', None)

def extract_sector(text):
    try:
        # Convertir la chaîne en dictionnaire Python
        data = ast.literal_eval(text)
        return data.get("Sector", None)  # Retourne "Sector" ou None si absent
    except (ValueError, SyntaxError):
        return None  # Si la conversion échoue, mettre None


jobs = jobs.loc[:,["Experience", "Qualifications","Salary Range","location","Country","Work Type","Company Size","Job Posting Date","Preference","Role","Job Portal","Benefits","skills","Company","Company Profile"]]

# TODO : Traitement de jobs Sector

# jobs["Sector"] = jobs["Company Profile"].apply(extract_sector)

# print(jobs["Sector"].iloc[0])

jobs = jobs.drop(columns=["Company Profile"])
#-----------------------------------------------------------------------------------------------

# d = ast.literal_eval(jobs["Company Profile"].iloc[0])
# print(d)
# print(type(d))
#
# pattern = r'"Sector"\s*:\s*"([^"]+)"'
#
# for i in range (0, len(jobs)):
#
#
# print(jobs["Sector"].iloc[0])
# Traitement Salary Range (Récupérer la moyenne)

