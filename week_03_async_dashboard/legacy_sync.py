import time
import httpx

# Usiamo un'API pubblica reale per simulare la latenza di rete
BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch_patient_profile(client: httpx.Client, patient_id: int) -> dict:
    """Simula una chiamata al Microservizio 'Anagrafica'"""
    print(f"🔄 [SYNC] Download profilo paziente {patient_id}...")
    response = client.get(f"{BASE_URL}/users/{patient_id}")
    response.raise_for_status()
    return response.json()

def fetch_patient_exams(client: httpx.Client, patient_id: int) -> list:
    """Simula una chiamata al Microservizio 'Cartelle Cliniche/Esami'"""
    print(f"🔄 [SYNC] Download esami paziente {patient_id}...")
    # Usiamo l'endpoint 'todos' per simulare una lista di esami da completare/completati
    response = client.get(f"{BASE_URL}/users/{patient_id}/todos")
    response.raise_for_status()
    return response.json()

def build_dashboard():
    print("🚀 START: Generazione Dashboard Pazienti (Lineare/Sincrona)")
    start_time = time.perf_counter()

    dashboard = []
    # Simuliamo la richiesta per 10 pazienti nel reparto
    patient_ids = list(range(1, 11))

    # Il Context Manager tiene viva la connessione TCP (Connection Pooling)
    with httpx.Client() as client:
        for pid in patient_ids:
            # COLLO DI BOTTIGLIA: Il programma si ferma qui ad aspettare la rete
            profile = fetch_patient_profile(client, pid)
            exams = fetch_patient_exams(client, pid)

            # Business logic: contiamo quanti esami sono completati
            completed = sum(1 for exam in exams if exam.get("completed"))

            dashboard.append({
                "name": profile.get("name"),
                "total_exams": len(exams),
                "completed_exams": completed
            })

    end_time = time.perf_counter()

    print("\n📊 --- DASHBOARD GENERATA ---")
    for entry in dashboard:
        print(f"👤 {entry['name']}: {entry['completed_exams']}/{entry['total_exams']} esami completati")

    print(f"\n⏱️ Tempo totale Sincrono: {end_time - start_time:.2f} secondi")

if __name__ == "__main__":
    build_dashboard()