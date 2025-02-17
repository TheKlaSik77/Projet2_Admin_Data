import pandas as pd
import os
import ast
import re


data_path = "./data/donnees_nettoyees.pkl"

# Charger depuis Pickle si le fichier existe, sinon lire le CSV et le sauvegarder
if os.path.exists(data_path):
    jobs = pd.read_pickle(data_path)
else:
    jobs = pd.read_csv("./data/donnees_nettoyees.csv", index_col=0)
    jobs.to_pickle(data_path)  # Sauvegarde pour la prochaine fois

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

print(jobs.columns)
#print(jobs["Sector"].value_counts())