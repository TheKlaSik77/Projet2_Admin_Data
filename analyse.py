import pandas as pd
import os
import ast
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


data_path = "./data/donnees_nettoyees.pkl"

# Charger depuis Pickle si le fichier existe, sinon lire le CSV et le sauvegarder
if os.path.exists(data_path):
    jobs = pd.read_pickle(data_path)
else:
    jobs = pd.read_csv("./data/donnees_nettoyees.csv", index_col=0)
    jobs.to_pickle(data_path)  # Sauvegarde pour la prochaine fois

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

jobs = jobs.iloc[:1000000]

jobs = pd.get_dummies(jobs, columns=['Work Type', 'Preference','Benefits'], drop_first=True)

# Définissons X et y, à savoir les paramètres et notre colonne à prédire
X = jobs.drop(columns=['Avg Salary','Sector','location','Country','Role','Company'])
y = jobs['Avg Salary']

# On split les données train et les données test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# On crée l'instance de RandomForestRegressor et on l'entraine
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Puis on le test sur l'ensemble de test pour faire des prédictions
y_pred = model.predict(X_test)

# On évalue les performances du modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}")
print(f"R2: {r2}")



#print(jobs["Sector"].value_counts())