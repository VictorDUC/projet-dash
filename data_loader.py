import yfinance as yf
from datetime import datetime, timedelta

def fetch_historical_data(symbol="BTC-USD", minutes=240):  # Nous allons récupérer les 120 dernières minutes (2 heures)
    """
    Récupère les données historiques du prix de la crypto sur les derniers 'minutes' spécifiés.
    
    Arguments:
        symbol (str): Symbole de la crypto (par exemple, 'BTC-USD' pour Bitcoin).
        minutes (int): Nombre de minutes de données à récupérer.
        
    Returns:
        timestamps (list): Liste des timestamps historiques.
        prices (list): Liste des prix historiques.
    """
    try:
        # Définir la date de début et la date de fin
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=minutes)  # Nous utilisons 'minutes' pour récupérer une fenêtre de 2h
        
        # Télécharger les données historiques de la crypto-monnaie
        data = yf.download(symbol, start=start_date, end=end_date, interval="1m")
        
        # Vérification de la structure des données récupérées
        print("Colonnes des données récupérées :", data.columns)  # Affiche les colonnes pour voir les niveaux de MultiIndex
        
        if ('Close', symbol) in data.columns:
            # Extraire les timestamps UNIX (en millisecondes)
            timestamps = [int(ts.timestamp()) * 1000 for ts in data.index]  # Convertir les index (dates) en timestamps UNIX en millisecondes
            # Extraire les prix de clôture (en utilisant le MultiIndex)
            prices = data[('Close', symbol)].tolist()

            # Afficher quelques timestamps pour débugger
            print(f"Quelques timestamps historiques : {timestamps[:5]}")  # Afficher les 5 premiers timestamps
            
            return timestamps, prices
        else:
            print("Erreur : La colonne 'Close' n'existe pas dans les données.")
            return [], []
    except Exception as e:
        print(f"Erreur lors de la récupération des données historiques : {e}")
        return [], []
