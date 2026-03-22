import time
from decorators import log_execution, retry
from mock_api import fake_data_fetch, NetworkError, RateLimitError

@log_execution
@retry(max_attempts=3, delay=1, exceptions=(NetworkError, RateLimitError))
def get_user_data(user_id: str):
    print(f"--- START: Richiesta dati utente {user_id} ---")
    result = fake_data_fetch(f"/users/{user_id}")
    print(f"--- SUCCESS: Dati ricevuti ---")
    return result

@log_execution
@retry(max_attempts=3, delay=1, exceptions=(NetworkError, RateLimitError))
def get_orders(user_id: str):
    print(f"--- START: Richiesta ordini {user_id} ---")
    result = fake_data_fetch(f"/orders/{user_id}")
    print(f"--- SUCCESS: Ordini ricevuti ---")
    return result