import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from ticker import start_ticker_stream
from callbacks import register_callbacks, prices, timestamps, lock
from data_loader import fetch_historical_data
from threading import Thread

# Crée l'application Dash
app = dash.Dash(__name__)

# Charge les données historiques au démarrage
def load_initial_data():
    global prices, timestamps, lock
    historical_timestamps, historical_prices = fetch_historical_data()
    if not historical_timestamps or not historical_prices:
        print("Erreur : Les données historiques n'ont pas pu être récupérées.")
        return False  # Retourner False si les données historiques échouent
    with lock:
        prices.extend(historical_prices)
        timestamps.extend(historical_timestamps)
    return True  # Retourner True si les données ont été récupérées avec succès

# Mise en page de l'application
app.layout = html.Div([
    html.H1("Prix du Bitcoin en Temps Réel"),
    dcc.Graph(id='live-graph', animate=False),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Mise à jour chaque seconde
        n_intervals=0
    )
])

# Enregistrement des callbacks
register_callbacks(app)

# Démarre le ticker et charge les données historiques
if __name__ == '__main__':
    if load_initial_data():  # Vérifie si les données historiques sont disponibles
        ticker_thread = Thread(target=start_ticker_stream)
        ticker_thread.start()
        app.run_server(debug=True)
    else:
        print("Impossible de démarrer l'application Dash, les données historiques sont manquantes.")
