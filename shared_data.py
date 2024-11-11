from threading import Lock

# Initialisation des prix, timestamps et du verrou pour synchronisation
prices = []
timestamps = []
lock = Lock()
