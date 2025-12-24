# Healthcare Chatbot

## Overview
This project is a multi-agent AI chatbot designed to assist with healthcare-related queries. It includes a backend built with FastAPI and a frontend built with React.

## Features
- Symptom Checker
- Appointment Scheduling
- Prescription Inquiry
- Emergency Guidance

## Setup Instructions

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
5. The backend will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. The frontend will be available at [http://localhost:5173](http://localhost:5173).

## Troubleshooting
- Ensure Node.js (v16.x or v18.x) and npm (v8.x or higher) are installed.
- If the frontend does not load, try clearing your browser cache or using an incognito window.
- Check for port conflicts and try running the frontend on a different port:
  ```bash
  npm run dev -- --port 3000
  ```

## Testing
1. Run backend tests:
   ```bash
   cd backend
   source venv/bin/activate
   python -m pytest test_main.py
   ```

## Notes
- Ensure the backend server is running before accessing the frontend.
- Update the `fetch` URL in `App.jsx` if the backend is hosted on a different address.

