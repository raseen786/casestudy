from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from lab45_autogen_extension.lab45aiplatform_autogen_extension import Lab45AIPlatformCompletionClient

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the request model
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class CustomCLient(Lab45AIPlatformCompletionClient):
    def close(self):
        # Custom processing of tool output can be implemented here
        pass

# Initialize the model client
model_client = CustomCLient(
    model="gpt-4o",
    base_url="https://api.waip.wiprocms.com/v1.1/",
    api_key="token|f5abf501-82b4-459b-86a0-8757826c9f7c|57d2d0a3754fc8bc17526d561d328185b0dc891b22c8b96f67702bc433451afc",
    enable_state_storage=True
)

# Define specialized agents
symptom_agent = AssistantAgent(
    "SymptomAgent",
    description="Analyzes symptoms and provides advice.",
    model_client=model_client,
    system_message="""
    You are a symptom analysis agent. Your job is to analyze symptoms provided by the user and give recommendations.
    """
)

appointment_agent = AssistantAgent(
    "AppointmentAgent",
    description="Manages appointment scheduling.",
    model_client=model_client,
    system_message="""
    You are an appointment management agent. Your job is to schedule, retrieve, and cancel appointments.
    you know the healthcare database structure and appointment logic.
    """
)

prescription_agent = AssistantAgent(
    "PrescriptionAgent",
    description="Provides prescription information.",
    model_client=model_client,
    system_message="""
    You are a prescription information agent. Your job is to provide details about medications.
    """
)

emergency_agent = AssistantAgent(
    "EmergencyAgent",
    description="Guides users during emergencies.",
    model_client=model_client,
    system_message="""
    You are an emergency guidance agent. Your job is to provide step-by-step instructions during emergencies.
    """
)

response_formatter_agent = AssistantAgent(
    "ResponseFormatterAgent",
    description="Formats responses for user queries.",
    model_client=model_client,
    system_message="""
    You are a response formatting agent. Your job is to ensure responses are clear and user-friendly.
    """
)

planning_agent = AssistantAgent(
    "PlanningAgent",
    description="Coordinates which agent should handle each query.",
    model_client=model_client,
    system_message="""
    You are a planning agent. Your job is to determine which specialized agent should handle the user query and when satisfied end with 'TERMINATE' key.
    """
)

# Define termination conditions
termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(max_messages=25)

# Create the team of agents
team = SelectorGroupChat(
    [planning_agent, symptom_agent, appointment_agent, prescription_agent, emergency_agent, response_formatter_agent],
    model_client=model_client,
    termination_condition=termination,
    allow_repeated_speaker=True
)

@app.post("/query")
async def handle_query(request: QueryRequest):
    """Handle user queries and delegate to the appropriate agent."""
    task = request.query
    result = ""  # Initialize result as an empty string
    async for message in team.run_stream(task=task):
        result += message  # Concatenate messages from the async generator
    return {"response": result}