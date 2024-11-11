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
            # Ajoute les nouvelles données uniquement si elles sont différentes de la dernière entrée
            if not prices or price != prices[-1] or timestamp != timestamps[-1]:
                prices.append(price)
                timestamps.append(timestamp)
                print(msg)  # Affiche les nouvelles données reçues pour vérification

# Fonction pour démarrer yliveticker dans un thread séparé
def start_ticker_stream():
    symbols = ["BTC-USD"]
    yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=symbols)
