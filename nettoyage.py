import pandas as pd
import os
import ast
import re
from sklearn.preprocessing import LabelEncoder

data_path = "./data/job_descriptions.pkl"

#test gaspard

# Charger depuis Pickle si le fichier existe, sinon lire le CSV et le sauvegarder
if os.path.exists(data_path):
    jobs = pd.read_pickle(data_path)
else:
    jobs = pd.read_csv("./data/job_descriptions.csv", index_col=None)
    jobs.to_pickle(data_path)  # Sauvegarde pour la prochaine fois

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


# Extrait le 'Sector'
def extract_sector(text):
    try:
        data = ast.literal_eval(text)
        return data.get("Sector", None)
    except (ValueError, SyntaxError):
        return None


# --------------------- Set de l'index à 'Job Id' et Gestion des Valeurs Manquantes ------------------------------

jobs = jobs.set_index('Job Id')

# missing_values = jobs.isnull().sum()
# print("Missing Values in Each Column:\n", missing_values)

# On remarque un faible pourcentage de missing_values pour 'Company Profile'. On remplit les missing values par "Unknown"
jobs["Company Profile"] = jobs["Company Profile"].fillna("Unknown")


# --------------------- Suppression des colonnes inutiles et Extraction de Sector dans une colonne ------------------------------


jobs = jobs.drop(['latitude', 'longitude','Job Posting Date', 'Contact Person', 'Contact', 'Job Title','Job Portal', 'Job Description','skills', 'Responsibilities'],axis=1)


jobs["Sector"] = jobs["Company Profile"].apply(extract_sector)

jobs = jobs.drop(columns=["Company Profile"])

# On supprime les lignes pour lesquelles Sector est vide
jobs = jobs.dropna(subset=["Sector"])

#------------------------ Traitement de Salaire en le transformant en Avg Salary -------------------------------

# Traitement Salary Range (Récupérer la moyenne)
jobs['Avg Salary'] = jobs['Salary Range'].str.replace(r'[K$]', '000', regex=True).str.extract(r'(\d+)-(\d+)').astype(float).mean(axis=1)
jobs = jobs.drop(columns=["Salary Range"])
#------------------------ Split de Experience en Experience Min et Max ----------------------------------------

# Traitement de Range Experience
jobs[["Experience_min", "Experience_max"]] = jobs["Experience"].str.extract(r'(\d+) to (\d+) Years')
jobs = jobs.drop(columns=["Experience"])

#--------------- Utilisation d'un 'Label Encodeur' pour encoder les colonnes catégorielles --------------------------
#------- afin de préparer le DataFrame au Random Forest qui ne fonctionne qu'avec des valeurs int -------------------

# On liste les colonnes catégorielles
colonnes_categorielles = ['Qualifications', 'location', 'Country', 'Work Type', 'Preference', 'Role', 'Benefits', 'Company', 'Sector']

# Puis, on les convertit en labels 'int'
label_encoders = {}     # Permets d'enregistrer les valeurs pour la convertion
for colonne in colonnes_categorielles:
    label_encoder = LabelEncoder()      # On crée l'instance de LabelEncoder()
    jobs[colonne] = label_encoder.fit_transform(jobs[colonne].astype('str'))      # Le label encoder va associer une valeur unique à chaque 'catégorie' trouvée
    label_encoders[colonne] = label_encoder     # On peut accéder à label_encoders[colonne].classes_ qui nous donnera la liste des valeurs dont l'index vaut la nouvelle valeur dans notre colonne

"""
Il existe un autre type d'encodage : le One-Hot Encoding qui crée une colonne par variable sous forme de booléen.
On aurait par exemple pour Country, une colonne par pays indiquant France : oui/non, Espagne : oui/non, etc...
Comme on a beaucoup de valeurs uniques, ça ferait beaucoup trop de colonnes à gérer.
"""
#---------------------------- Affichages de fin -----------------------------------------------


# Calcul du nombre de lignes contenant au moins une valeur NaN
print(f"Nombre de valeurs vides par colonnes : \n{jobs.isna().sum()}")

# Calcul du nombre total de lignes
print(f"\nNombre total de lignes : {len(jobs)}\n")

print(f"Affichage des 5 premières lignes : \n{jobs.head()}")

jobs.to_csv("./data/donnees_nettoyees.csv", index=0)

