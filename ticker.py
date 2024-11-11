import yliveticker
from threading import Lock
from callbacks import prices, timestamps, lock

# Fonction appelée pour chaque mise à jour en temps réel
def on_new_msg(ws, msg):
    global prices, timestamps, lock

    price = msg.get("price")
    timestamp = msg.get("timestamp")

    if price is not None and timestamp is not None:
        with lock:
            # Si nous avons déjà des données historiques, alignons le timestamp en temps réel avec le dernier historique
            if timestamps:
                # Aligner le timestamp en temps réel avec le dernier timestamp historique
                # On ajuste le timestamp en temps réel pour qu'il commence juste après les données historiques
                adjusted_timestamp = timestamps[-1] + (timestamp - timestamps[-1])
            else:
                # Si pas encore de données historiques, utiliser le timestamp tel quel
                adjusted_timestamp = timestamp

            # Ajoute les nouvelles données uniquement si elles sont différentes de la dernière entrée
            if not prices or price != prices[-1] or adjusted_timestamp != timestamps[-1]:
                prices.append(price)
                timestamps.append(adjusted_timestamp)
                print(msg)  # Affiche les nouvelles données reçues pour vérification

# Fonction pour démarrer yliveticker dans un thread séparé
def start_ticker_stream():
    symbols = ["BTC-USD"]
    yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=symbols)
