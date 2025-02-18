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

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def extract_sector(text):
    try:
        # Convertir la chaîne en dictionnaire Python
        data = ast.literal_eval(text)
        return data.get("Sector", None)  # Retourne "Sector" ou None si absent
    except (ValueError, SyntaxError):
        return None  # Si la conversion échoue, mettre None


jobs = jobs.loc[:,["Experience", "Qualifications","Salary Range","location","Country","Work Type","Company Size","Preference","Role","Benefits","Company","Company Profile"]]

# Fixme : Traitement de jobs Sector

jobs["Sector"] = jobs["Company Profile"].apply(extract_sector)

#-----------------------------------------------------------------------------------------------

# Fixme : Traitement Salary Range (Récupérer la moyenne)
jobs['Avg Salary'] = jobs['Salary Range'].str.replace(r'[K$]', '000', regex=True).str.extract(r'(\d+)-(\d+)').astype(float).mean(axis=1)


#-------------------------------------------------------------------------------------------------

# Fixme : Traitement de Range Experience
jobs[["Experience min", "Experience_max"]] = jobs["Experience"].str.extract(r'(\d+) to (\d+) Years')

jobs = jobs.drop(columns=["Company Profile","Salary Range","Experience"])

jobs.to_csv("./data/donnees_nettoyees.csv", index=False)

