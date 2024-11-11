import plotly.graph_objs as go
from dash.dependencies import Output, Input
from shared_data import prices, timestamps, lock  # Importation depuis shared_data.py

# Fonction pour enregistrer les callbacks
def register_callbacks(app):
    @app.callback(
        Output('live-graph', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n):
        global prices, timestamps, lock

        # Utiliser les données déjà chargées, pas besoin de refaire fetch_historical_data
        with lock:
            # Copie les données pour éviter les conflits
            current_prices = prices.copy()
            current_timestamps = timestamps.copy()

        # Crée le graphique avec les données en temps réel et historiques
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

            # Réajustement de l'axe des X pour une plage plus dynamique
            if len(current_timestamps) > 1:
                time_margin = (current_timestamps[-1] - current_timestamps[0]) * 0.05
                x_min = current_timestamps[0] - time_margin
                x_max = current_timestamps[-1] + time_margin

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