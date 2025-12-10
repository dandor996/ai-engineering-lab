import statistics
from dataclasses import dataclass
from typing import Union, Optional, Any
from enum import Enum
from datetime import datetime

# --- Domain Constants ---
MAX_SYS_BP = 135
MAX_DIA_BP = 85
MIN_HEART_RATE = 50
MAX_HEART_RATE = 100


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


# Mock data representing legacy database export
# Contains inconsistent types and missing fields to simulate dirty data
raw_patients_data: list[dict[str, Any]] = [
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
            # Edge case: 'value' is a dict here, but float/int elsewhere
            {"date": "2023-10-05", "type": "blood_pressure", "value": {"sys": 140, "dia": 90}},
        ]
    },
    {
        "id": "P003",
        "details": {"name": "Anna Bianchi", "age": 30},
        "history": []
    }
]

def parse_patient(raw_data: dict[str, Any]) -> Patient:
    """
    Parses raw patient dictionary into a structured Patient object.
    
    Handles defensive data extraction:
    - Returns default values for missing patient details.
    - Skips malformed or incomplete exams.
    - Normalizes inconsistent data types.
    """
    p_id = raw_data.get("id", "NO_ID")
    details = raw_data.get("details", {})
    p_name = details.get("name", "N/A")
    p_age = details.get("age", 0)

    clean_history_list: list[Exam] = []
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
                        print(f"Skipping invalid BP values: {raw_value}")
                else:
                    print(f"Skipping incomplete BP record: {raw_value}")

        elif exam_type == ExamType.HEART_RATE:
            # Handle cases where value might be string or float
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

def analyze_patient_health(patients: list[Patient]) -> list[str]:
    """
    Generates health alerts based on patient history.
    
    Uses Type Narrowing (isinstance) to safely access the specific attributes
    of the polymorphic 'value' field (BloodPressure, HeartRate, etc.).
    """
    alerts = []

    for patient in patients:
        print(f"Analyzing {patient.name} ({patient.id})...")
        sys_pressures: list[int] = []

        for exam in patient.history:
            # Type Narrowing allows safe access to specific dataclass fields
            if isinstance(exam.value, BloodPressure):
                bp = exam.value
                sys = bp.sys
                dia = bp.dia

                if sys > MAX_SYS_BP or dia > MAX_DIA_BP:
                    alerts.append(f"HYPERTENSION ALERT: {patient.name} - {bp.sys}/{bp.dia}")
                sys_pressures.append(sys)

            elif isinstance(exam.value, HeartRate):
                hr = exam.value.val
                if hr > MAX_HEART_RATE or hr < MIN_HEART_RATE:
                    alerts.append(f"ABNORMAL HR ALERT: {patient.name} - {hr} bpm")

        if sys_pressures:
            avg_sys = statistics.mean(sys_pressures)
            print(f"  -> Avg Systolic BP: {avg_sys:.1f}")
        else:
            print("  -> No BP data available.")

    return alerts


if __name__ == "__main__":
    # Transformation (ETL)
    clean_patients_data: list[Patient] = []
    for raw_p in raw_patients_data:
        clean_patients_data.append(parse_patient(raw_p))

    # Analysis
    risk_report = analyze_patient_health(clean_patients_data)

    # Reporting
    print("\n--- HEALTH REPORT ---")
    for alert in risk_report:
        print(alert)