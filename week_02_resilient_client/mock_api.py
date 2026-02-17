import random
import time

class NetworkError(Exception):
    pass

class RateLimitError(Exception):
    pass

def fake_data_fetch(endpoint: str):
    """Simula una chiamata API instabile."""
    print(f"  -> Tentativo connessione a {endpoint}...")
    time.sleep(0.5)  # Latenza
    
    roll = random.random()
    if roll < 0.3:
        raise NetworkError("Connection timed out")
    elif roll < 0.5:
        raise RateLimitError("429 Too Many Requests")
    elif roll < 0.6:
        raise ValueError("500 Internal Server Error (Fatal)")
    
    return {"status": 200, "data": [1, 2, 3, 4], "source": endpoint}