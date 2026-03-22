from client_legacy import get_user_data, get_orders

def main():
    user_id = "12345"
    
    try:
        user_data = get_user_data(user_id)
        print(f"Dati utente: {user_data}")
        
        orders = get_orders(user_id)
        print(f"Ordini: {orders}")
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        
if __name__ == "__main__":
    main()

    