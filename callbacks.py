import plotly.graph_objs as go
from dash.dependencies import Output, Input
from threading import Lock

# Initialisation des prix, timestamps et du verrou pour synchronisation
prices = []
timestamps = []
lock = Lock()

# Fonction pour enregistrer les callbacks
def register_callbacks(app):
    @app.callback(
        Output('live-graph', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n):
        global prices, timestamps, lock

        with lock:
            # Copie les données pour éviter les conflits
            current_prices = prices.copy()
            current_timestamps = timestamps.copy()

        fig = go.Figure(data=[go.Scatter(
            x=current_timestamps,
            y=current_prices,
            mode='lines+markers',
            name='BTC-USD'
        )])

        if current_timestamps and current_prices:
            x_min, x_max = min(current_timestamps), max(current_timestamps)
            y_min, y_max = min(current_prices), max(current_prices)
            y_range = y_max - y_min
            y_margin = y_range * 0.05  # Marge de 5%

            fig.update_layout(
                xaxis=dict(title="Temps", range=[x_min, x_max]),
                yaxis=dict(title="Prix (USD)", range=[y_min - y_margin, y_max + y_margin]),
                title="Prix du Bitcoin (BTC-USD) en Temps Réel",
                showlegend=False
            )
        else:
            fig.update_layout(
                title="Prix du Bitcoin (BTC-USD) en Temps Réel",
                yaxis_title="Prix (USD)",
                showlegend=False
            )

        return fig
