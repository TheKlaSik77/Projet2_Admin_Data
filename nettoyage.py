import pandas as pd
import os
import ast
import re


data_path = "./data/job_descriptions.pkl"

# Charger depuis Pickle si le fichier existe, sinon lire le CSV et le sauvegarder
if os.path.exists(data_path):
    jobs = pd.read_pickle(data_path)
else:
    jobs = pd.read_csv("./data/job_descriptions.csv", index_col=0)
    jobs.to_pickle(data_path)  # Sauvegarde pour la prochaine fois

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def extract_sector(text):
    try:
        # Convertir la chaîne en dictionnaire Python
        data = ast.literal_eval(text)
        return data.get("Sector", None)  # Retourne "Sector" ou None si absent
    except (ValueError, SyntaxError):
        return None  # Si la conversion échoue, mettre None


jobs = jobs.loc[:,["Experience", "Qualifications","Salary Range","location","Country","Work Type","Company Size","Job Posting Date","Preference","Role","Benefits","Company","Company Profile"]]

# Fixme : Traitement de jobs Sector

# jobs["Sector"] = jobs["Company Profile"].apply(extract_sector)

# print(jobs["Sector"].iloc[0])

# print(jobs.head())
#-----------------------------------------------------------------------------------------------

# Fixme : Traitement Salary Range (Récupérer la moyenne)
# jobs['Avg Salary'] = jobs['Salary Range'].str.replace(r'[K$]', '000', regex=True).str.extract(r'(\d+)-(\d+)').astype(float).mean(axis=1)
# print(jobs[["Salary Range","Salary"]].head())

print(jobs.columns)
print(jobs["Experience"].head())

#-------------------------------------------------------------------------------------------------

# Fixme : Traitement de Range Experience
# jobs[["Experience min", "Experience_max"]] = jobs["Experience"].str.extract(r'(\d+) to (\d+) Years')
# print(jobs[["Experience min", "Experience_max","Experience"]].head())
# jobs = jobs.drop(columns=["Company Profile","Salary Range,"Experience"])