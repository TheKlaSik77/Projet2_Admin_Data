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

# Extrait les Sector
def extract_sector(text):
    try:
        data = ast.literal_eval(text)
        return data.get("Sector", None)
    except (ValueError, SyntaxError):
        return None

jobs = jobs.drop(['latitude', 'longitude','Job Posting Date', 'Contact Person', 'Contact', 'Job Title','Job Portal', 'Job Description','skills', 'Responsibilities'],axis=1)
# Fixme : Traitement de jobs Sector

jobs["Sector"] = jobs["Company Profile"].apply(extract_sector)

#-----------------------------------------------------------------------------------------------

# Traitement Salary Range (Récupérer la moyenne)
jobs['Avg Salary'] = jobs['Salary Range'].str.replace(r'[K$]', '000', regex=True).str.extract(r'(\d+)-(\d+)').astype(float).mean(axis=1)


#-------------------------------------------------------------------------------------------------

# Traitement de Range Experience
jobs[["Experience_min", "Experience_max"]] = jobs["Experience"].str.extract(r'(\d+) to (\d+) Years')

jobs = jobs.drop(columns=["Company Profile","Salary Range","Experience"])

jobs.fillna("Inconnu", inplace=True)

jobs.to_csv("./data/donnees_nettoyees.csv", index=False)

