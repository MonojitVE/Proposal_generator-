import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from pipeline import generate_proposal


app = FastAPI(title="Proposal Generator API")


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------
class ProposalRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    description: str
    project_type: str = ""
    industry: str = ""
    timeline: str = ""
    budget: str = ""
    phases: str = ""
    resources: str = ""
    client_name: str = ""
    extra_requirements: str = ""
    include_flow_diagram: bool = False


# -----------------------------
# Response Model
# -----------------------------
class ProposalResponse(BaseModel):
    proposal_text: str


# -----------------------------
# Health / Root
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Proposal Generator API is running",
        "health": "/health",
        "generate": "/generate",
    }


@app.get("/health")
def health():
    return {
        "status": "Proposal Generator API is running"
    }


# -----------------------------
# Generate Proposal
# -----------------------------
@app.post("/generate", response_model=ProposalResponse)
def generate(req: ProposalRequest):

    if not req.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Project description is required."
        )

    enriched_input = f"""
Project Description: {req.description}
{f"Project Type: {req.project_type}" if req.project_type else ""}
{f"Industry/Domain: {req.industry}" if req.industry else ""}
{f"Timeline: {req.timeline}" if req.timeline else ""}
{f"Budget: {req.budget}" if req.budget else ""}
{f"Phases: {req.phases}" if req.phases else ""}
{f"Resources: {req.resources}" if req.resources else ""}
{f"Client: {req.client_name}" if req.client_name else ""}
{f"Additional Requirements: {req.extra_requirements}" if req.extra_requirements else ""}
""".strip()

    try:
        proposal_text = generate_proposal(
            enriched_input,
            user_timeline=req.timeline,
            user_budget=req.budget,
            user_phases=req.phases,
            user_resources=req.resources,
            include_flow_diagram=req.include_flow_diagram,
        )

        return ProposalResponse(
            proposal_text=proposal_text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Local Development
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )