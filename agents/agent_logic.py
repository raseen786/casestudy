from typing import Dict, Any

class SymptomCheckerAgent:
    @staticmethod
    def analyze_symptoms(symptoms: list[str], duration: str, severity: int) -> Dict[str, Any]:
        # Placeholder logic for symptom analysis
        return {
            "advice": "Please consult a healthcare professional for a proper diagnosis.",
            "recommendations": ["Rest", "Stay hydrated", "Monitor symptoms"]
        }

class AppointmentManagerAgent:
    @staticmethod
    def schedule_appointment(doctor_name: str, specialty: str, preferred_date: str, user_id: str) -> Dict[str, Any]:
        # Placeholder logic for appointment scheduling
        return {
            "appointment_id": "APT-12345",
            "status": "Appointment scheduled successfully"
        }

    @staticmethod
    def get_appointments(user_id: str) -> Dict[str, Any]:
        # Placeholder logic for retrieving appointments
        return {
            "appointments": [
                {
                    "appointment_id": "APT-12345",
                    "doctor_name": "Dr. Lee",
                    "date": "2025-12-28",
                    "time": "10:00 AM"
                }
            ]
        }

    @staticmethod
    def cancel_appointment(appointment_id: str) -> Dict[str, Any]:
        # Placeholder logic for canceling appointments
        return {
            "appointment_id": appointment_id,
            "status": "Appointment cancelled successfully"
        }

class PrescriptionAgent:
    @staticmethod
    def get_prescription_info(medication_name: str) -> Dict[str, Any]:
        # Placeholder logic for prescription inquiries
        return {
            "dosage": "500mg",
            "frequency": "Twice daily",
            "side_effects": ["Nausea", "Headache"],
            "warnings": "Do not take with alcohol"
        }

class EmergencyAgent:
    @staticmethod
    def provide_guidance(emergency_type: str, description: str) -> Dict[str, Any]:
        # Placeholder logic for emergency guidance
        return {
            "steps": [
                "Step 1: Call emergency services immediately (911)",
                "Step 2: Keep the person calm and comfortable",
                "Step 3: Follow dispatcher instructions"
            ],
            "follow_up": "Seek immediate medical attention"
        }

class PlanningAgent:
    @staticmethod
    def route_query(query: str) -> str:
        # Improved routing logic based on keywords in the query
        query = query.lower()
        if "headache" in query or "symptom" in query:
            return "SymptomCheckerAgent"
        elif "appointment" in query or "schedule" in query:
            return "AppointmentManagerAgent"
        elif "ibuprofen" in query or "prescription" in query:
            return "PrescriptionAgent"
        elif "emergency" in query:
            return "EmergencyAgent"
        else:
            return "UnknownAgent"