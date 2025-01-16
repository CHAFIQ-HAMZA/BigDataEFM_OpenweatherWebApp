import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
def get_data_and_partial_cleaning():
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:example@localhost:27017/?authSource=admin")  # Remplacez par votre URI MongoDB
    db = client["weather_db"]  # Nom de la base de données
    collection = db["forecast_data"]  # Nom de la collection

    # Lecture des données depuis MongoDB
    cursor = collection.find()  # Filtres si nécessaire
    df = pd.DataFrame(list(cursor))  # Conversion en DataFrame

    # Nettoyage des données (par exemple, suppression de l'_id si inutile)
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)

    # Nettoyage des données
    df = df.drop_duplicates()
    df = df.dropna()
    df = df.dropna(subset=['température', 'précipitations', 'neige'])
    if "horodatage" in df.columns:
        df["horodatage"] = pd.to_datetime(df["horodatage"], errors='coerce')

    dates_invalides = df[df['horodatage'].isna()]
    stats_temp = df.groupby('ville')[['température', 'température_minimale', 'température_maximale']].agg(
        ['mean', 'min', 'max'])

    df['temps_formaté'] = pd.to_datetime(df['temps_formaté'])
    return df;