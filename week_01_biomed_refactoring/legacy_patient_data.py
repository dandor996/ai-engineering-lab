import statistics

# SIMULAZIONE DATABASE (LEGACY DATA DUMP)
# Un incubo di dizionari annidati senza schema garantito.
raw_patients_data = [
    {
        "id": "P001",
        "details": {"name": "Mario Rossi", "age": 45},
        "history": [
            {"date": "2023-10-01", "type": "heart_rate", "value": 72},
            {"date": "2023-10-01", "type": "blood_pressure", "value": {"sys": 120, "dia": 80}},
        ]
    },
    {
        "id": "P002",
        "details": {"name": "Luigi Verdi", "age": 60},
        "history": [
            {"date": "2023-10-02", "type": "glucose", "value": 95.5},
            # Nota: qui "value" è un dict, sopra era un int o float. Inconsistenza!
            {"date": "2023-10-05", "type": "blood_pressure", "value": {"sys": 140, "dia": 90}},
        ]
    },
    {
        "id": "P003",
        "details": {"name": "Anna Bianchi", "age": 30},
        "history": [] # Nessun dato storico
    }
]

def analyze_patient_health(data):
    """
    Funzione monolitica che cerca di estrarre insight dai dati sporchi.
    Tutto basato su stringhe magiche e accessi a dizionari.
    """
    alerts = []
    
    for patient in data:
        p_id = patient["id"]
        # Accesso fragile: se manca "details" o "name", crasha.
        name = patient["details"]["name"] 
        exams = patient.get("history", [])
        
        print(f"Analyzing {name} ({p_id})...")
        
        sys_pressures = []
        
        for exam in exams:
            # Logica condizionale basata su stringhe (Error Prone)
            if exam["type"] == "blood_pressure":
                # Qui assumiamo che value sia un dict. Se fosse None? Crash.
                bp = exam["value"]
                sys = bp["sys"]
                dia = bp["dia"]
                
                if sys > 135 or dia > 85:
                    alerts.append(f"ALERTA IPERTENSIONE: {name} - {sys}/{dia}")
                
                sys_pressures.append(sys)
            
            elif exam["type"] == "heart_rate":
                # Qui assumiamo che value sia un int
                hr = exam["value"]
                if hr > 100 or hr < 50:
                    alerts.append(f"ALERTA BATTITO: {name} - {hr} bpm")

        if sys_pressures:
            avg_sys = statistics.mean(sys_pressures)
            print(f"  -> Media Pressione Sistolica: {avg_sys:.1f}")
        else:
            print("  -> Nessun dato pressorio.")

    return alerts

# MAIN DI ESECUZIONE
if __name__ == "__main__":
    risk_report = analyze_patient_health(raw_patients_data)
    print("\n--- REPORT GENERATO ---")
    for alert in risk_report:
        print(alert)