import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from ticker import start_ticker_stream  # Import de la fonction pour démarrer le stream
from callbacks import register_callbacks  # Import de la fonction pour enregistrer les callbacks
from threading import Thread

# Crée l'application Dash
app = dash.Dash(__name__)

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

# Démarre yliveticker dans un thread séparé
if __name__ == '__main__':
    ticker_thread = Thread(target=start_ticker_stream)
    ticker_thread.start()
    app.run_server(debug=True)
