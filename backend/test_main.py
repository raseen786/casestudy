from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from .database import SessionLocal, Appointment, Prescription

client = TestClient(app)

# Helper function to populate the database for testing
def setup_test_data():
    db = SessionLocal()
    db.query(Appointment).delete()
    db.query(Prescription).delete()

    # Add a test appointment
    test_appointment = Appointment(
        user_id="user123",
        doctor_name="Dr. Smith",
        specialty="Cardiology",
        date=datetime(2025, 12, 30),
        status="Scheduled"
    )
    db.add(test_appointment)

    # Add a test prescription
    test_prescription = Prescription(
        user_id="user123",
        medication_name="Ibuprofen",
        dosage="500mg",
        frequency="Twice daily",
        side_effects="Nausea,Headache",
        warnings="Do not take with alcohol"
    )
    db.add(test_prescription)

    db.commit()
    db.close()

setup_test_data()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Healthcare Chatbot API!"}

def test_schedule_appointment():
    response = client.post(
        "/appointments",
        json={
            "doctor_name": "Dr. Smith",
            "specialty": "Cardiology",
            "preferred_date": "2025-12-30",
            "user_id": "user123"
        }
    )
    assert response.status_code == 200
    assert "appointment_id" in response.json()

def test_get_appointments():
    user_id = "user123"
    response = client.get(f"/appointments/{user_id}")
    assert response.status_code == 200
    assert "appointments" in response.json()

def test_cancel_appointment():
    appointment_id = "1"
    response = client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "Appointment cancelled successfully"

def test_prescription_inquiry():
    response = client.post(
        "/prescriptions",
        json={"medication_name": "Ibuprofen"}
    )
    assert response.status_code == 200
    assert "dosage" in response.json()

def test_handle_query_symptom_checker():
    response = client.post(
        "/query",
        json={"query": "I have a headache", "user_id": "user123"}
    )
    assert response.status_code == 200
    assert "advice" in response.json()

def test_handle_query_appointment_manager():
    response = client.post(
        "/query",
        json={"query": "Check my appointments", "user_id": "user123"}
    )
    assert response.status_code == 200
    assert "appointments" in response.json()

def test_handle_query_prescription_agent():
    response = client.post(
        "/query",
        json={"query": "Tell me about Ibuprofen", "user_id": "user123"}
    )
    assert response.status_code == 200
    assert "dosage" in response.json()

def test_handle_query_emergency_agent():
    response = client.post(
        "/query",
        json={"query": "What to do in an emergency?", "user_id": "user123"}
    )
    assert response.status_code == 200
    assert "steps" in response.json()