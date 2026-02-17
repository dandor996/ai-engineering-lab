import time
from mock_api import fake_data_fetch, NetworkError, RateLimitError

def get_user_data(user_id: str):
    print(f"--- START: Richiesta dati utente {user_id} ---")
    retries = 3
    delay = 1
    attempt = 0
    
    while attempt < retries:
        try:
            result = fake_data_fetch(f"/users/{user_id}")
            print(f"--- SUCCESS: Dati ricevuti ---")
            return result
        except (NetworkError, RateLimitError) as e:
            attempt += 1
            print(f"⚠️ Errore transitorio: {e}. Riprovo tra {delay}s ({attempt}/{retries})")
            time.sleep(delay)
            delay *= 2  # Exponential backoff manuale
        except Exception as e:
            print(f"🔥 Errore fatale: {e}")
            raise
    
    print("❌ Tentativi esauriti.")
    raise NetworkError("Max retries exceeded")

def get_orders(user_id: str):
    # BOILERPLATE DUPLICATO!
    print(f"--- START: Richiesta ordini {user_id} ---")
    retries = 3
    delay = 1
    attempt = 0
    
    while attempt < retries:
        try:
            result = fake_data_fetch(f"/orders/{user_id}")
            print(f"--- SUCCESS: Ordini ricevuti ---")
            return result
        except (NetworkError, RateLimitError) as e:
            attempt += 1
            print(f"⚠️ Errore transitorio: {e}. Riprovo tra {delay}s ({attempt}/{retries})")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            print(f"🔥 Errore fatale: {e}")
            raise
            
    raise NetworkError("Max retries exceeded")