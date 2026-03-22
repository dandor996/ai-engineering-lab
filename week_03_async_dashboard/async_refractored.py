import time
import httpx
import asyncio

BASE_URL = "https://jsonplaceholder.typicode.com"

async def fetch_patient_profile(client: httpx.AsyncClient, patient_id: int) -> dict:
    """
    Asynchronously fetch patient profile from Master Data Microservice.
    """
    print(f"🔄 [ASYNC] Downloading patient profile {patient_id}...")
    response = await client.get(f"{BASE_URL}/users/{patient_id}")
    response.raise_for_status()
    return response.json()


async def fetch_patient_exams(client: httpx.AsyncClient, patient_id: int) -> list:
    """
    Asynchronously fetch patient medical exams from Records Microservice.
    """
    print(f"🔄 [ASYNC] Downloading patient exams for {patient_id}...")
    response = await client.get(f"{BASE_URL}/users/{patient_id}/todos")
    response.raise_for_status()
    return response.json()


async def get_single_patient_data(client: httpx.AsyncClient, pid: int) -> dict:
    """
    Aggregate data for a single patient by fetching profile and exams concurrently.
    """
    profile, exams = await asyncio.gather( 
        fetch_patient_profile(client, pid),
        fetch_patient_exams(client, pid)
    )
    
    completed = sum(1 for exam in exams if exam.get("completed"))

    return {
        "name": profile.get("name"),
        "total_exams": len(exams),
        "completed_exams": completed
    }


async def build_dashboard():
    """
    Generate a patient dashboard by concurrently fetching data for all patients.
    """
    print("🚀 START: Patient Dashboard Generation (Asynchronous)")
    start_time = time.perf_counter()

    patient_ids = list(range(1, 11)) + [9999]  # 10 valid patients + 1 invalid to test error handling

    async with httpx.AsyncClient() as client:
        tasks = [get_single_patient_data(client, pid) for pid in patient_ids]

        dashboard = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = time.perf_counter()

    print("\n📊 --- DASHBOARD GENERATED ---")
    for entry in dashboard:
        if isinstance(entry, Exception):
            print(f"❌ Error fetching data: {entry}")
        else:
            print(f"👤 {entry['name']}: {entry['completed_exams']}/{entry['total_exams']} exams completed")
        
    elapsed = end_time - start_time
    print(f"\n⏱️ Total time (asynchronous): {elapsed:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(build_dashboard())
