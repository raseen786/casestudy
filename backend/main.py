from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db, Appointment, Prescription
from datetime import datetime
from agents.agent_logic import SymptomCheckerAgent, AppointmentManagerAgent, PrescriptionAgent, EmergencyAgent, PlanningAgent

app = FastAPI()

# Request models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class SymptomRequest(BaseModel):
    symptoms: List[str]
    duration: str
    severity: int  # 1-10

class AppointmentRequest(BaseModel):
    doctor_name: str
    specialty: str
    preferred_date: str
    user_id: str

class PrescriptionRequest(BaseModel):
    medication_name: str
    user_id: Optional[str] = None

class EmergencyRequest(BaseModel):
    emergency_type: str
    description: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare Chatbot API!"}

# Query endpoint
@app.post("/query")
def handle_query(request: QueryRequest):
    """Handle general user queries and route to appropriate agent."""
    agent_name = PlanningAgent.route_query(request.query)

    if agent_name == "SymptomCheckerAgent":
        return SymptomCheckerAgent.analyze_symptoms([], "", 0)  # Placeholder
    elif agent_name == "AppointmentManagerAgent":
        return AppointmentManagerAgent.get_appointments(request.user_id)
    elif agent_name == "PrescriptionAgent":
        return PrescriptionAgent.get_prescription_info("Placeholder")
    elif agent_name == "EmergencyAgent":
        return EmergencyAgent.provide_guidance("", "")  # Placeholder
    else:
        return {"error": "Unknown query type"}

# Symptom Checker endpoint
@app.post("/symptom-check")
def symptom_check(request: SymptomRequest):
    """Analyze symptoms and provide preliminary advice."""
    return {
        "symptoms": request.symptoms,
        "duration": request.duration,
        "severity": request.severity,
        "advice": "Please consult a healthcare professional for a proper diagnosis.",
        "recommendations": ["Rest", "Stay hydrated", "Monitor symptoms"]
    }

# Appointment Scheduling endpoint
@app.post("/appointments")
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    """Book an appointment with a healthcare provider."""
    appointment_date = datetime.strptime(request.preferred_date, "%Y-%m-%d")
    appointment = Appointment(
        user_id=request.user_id,
        doctor_name=request.doctor_name,
        specialty=request.specialty,
        date=appointment_date,
        status="Scheduled"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {
        "appointment_id": appointment.id,
        "doctor_name": appointment.doctor_name,
        "specialty": appointment.specialty,
        "preferred_date": appointment.date,
        "status": appointment.status
    }

# Get appointments endpoint
@app.get("/appointments/{user_id}")
def get_appointments(user_id: str, db: Session = Depends(get_db)):
    """Retrieve user's scheduled appointments."""
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
    return {
        "user_id": user_id,
        "appointments": [
            {
                "appointment_id": appt.id,
                "doctor_name": appt.doctor_name,
                "date": appt.date,
                "status": appt.status
            } for appt in appointments
        ]
    }

# Cancel appointment endpoint
@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: str, db: Session = Depends(get_db)):
    """Cancel a scheduled appointment."""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
        return {
            "appointment_id": appointment_id,
            "status": "Appointment cancelled successfully"
        }
    return {"error": "Appointment not found"}

# Prescription Inquiry endpoint
@app.post("/prescriptions")
def prescription_inquiry(request: PrescriptionRequest, db: Session = Depends(get_db)):
    """Get information about medications."""
    prescription = db.query(Prescription).filter(Prescription.medication_name == request.medication_name).first()
    if prescription:
        return {
            "medication_name": prescription.medication_name,
            "dosage": prescription.dosage,
            "frequency": prescription.frequency,
            "side_effects": prescription.side_effects.split(","),
            "warnings": prescription.warnings
        }
    return {"error": "Prescription not found"}

# Emergency Guidance endpoint
@app.post("/emergency")
def emergency_guidance(request: EmergencyRequest):
    """Provide step-by-step guidance for emergency situations."""
    return {
        "emergency_type": request.emergency_type,
        "steps": [
            "Step 1: Call emergency services immediately (911)",
            "Step 2: Keep the person calm and comfortable",
            "Step 3: Follow dispatcher instructions"
        ],
        "follow_up": "Seek immediate medical attention"
    }