import statistics
from dataclasses import dataclass
from typing import Union, Optional, Any
from enum import Enum
from datetime import datetime

class ExamType(Enum):
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE = "blood_pressure"
    GLUCOSE = "glucose"


@dataclass
class BloodPressure:
    sys: int
    dia: int


@dataclass
class HeartRate:
    val: int


@dataclass
class Glucose:
    val: float


@dataclass
class Exam:
    date: datetime
    type: ExamType
    value: Union[BloodPressure, HeartRate, Glucose]


@dataclass
class Patient:
    id: str
    name: str
    age: int
    history: list[Exam]


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

def parse_patient(raw_data: dict[str, Any]) -> Patient:
    """
    Converts raw dictionary data into a type-safe Patient object.
    Implements defensive programming to handle missing keys or bad types.
    """
    # Estrazione dizionari
    p_id = raw_data.get("id", "NO_ID")
    details = raw_data.get("details", {})

    # Estrazione singoli campi in details
    p_name = details.get("name", "N/A")
    p_age = details.get("age", 0)

    clean_history_list: list[Exam] = []

    # Estrazione singoli campi in history
    raw_history_list = raw_data.get("history", [])

    for raw_exam in raw_history_list:
        raw_date = raw_exam.get("date")
        try:
            date = datetime.strptime(raw_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue

        raw_type = raw_exam.get("type")
        try:
            exam_type = ExamType(raw_type)
        except ValueError:
            continue

        raw_value = raw_exam.get("value")
        if raw_value is None:
            continue

        value: BloodPressure | HeartRate | Glucose | None = None

        if exam_type == ExamType.BLOOD_PRESSURE:
            if isinstance(raw_value, dict):
                if "sys" in raw_value and "dia" in raw_value:
                    try:
                        sys = raw_value.get("sys", 0)
                        dia = raw_value.get("dia", 0)
                        value = BloodPressure(sys=sys, dia=dia)
                    except (ValueError, TypeError):
                        print(f"Valor pressione non numerici: {raw_value}")
                else:
                    print(f"Dati pressione incompleti (mancano chiavi): {raw_value}")

        elif exam_type == ExamType.HEART_RATE:
            try:
                hr = int(raw_value)
                value = HeartRate(val=hr)
            except (ValueError, TypeError):
                continue
        elif exam_type == ExamType.GLUCOSE:
            try:
                gl = float(raw_value)
                value = Glucose(val=gl)
            except (ValueError, TypeError):
                continue

        if value is not None:
            clean_exam = Exam(date=date, type=exam_type, value=value)
            clean_history_list.append(clean_exam)

    return Patient(id=p_id, name=p_name, age=p_age, history=clean_history_list)

def analyze_patient_health(data):
    """
    LEGACY FUNCTION: Still uses dictionary access.
    Will be refactored in next step to use Patient objects.
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