import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pipeline import generate_proposal
from pdf_generator import create_proposal_pdf
import io

app = FastAPI(title="Proposal Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProposalRequest(BaseModel):
    description: str
    project_type: str = ""
    industry: str = ""
    timeline: str = ""
    budget: str = ""
    client_name: str = ""
    extra_requirements: str = ""


class ProposalResponse(BaseModel):
    proposal_text: str


@app.get("/")
def root():
    return {"status": "Proposal Generator API is running"}


@app.post("/generate", response_model=ProposalResponse)
def generate(req: ProposalRequest):
    if not req.description.strip():
        raise HTTPException(status_code=400, detail="Project description is required.")

    enriched_input = f"""
Project Description: {req.description}
{f"Project Type: {req.project_type}" if req.project_type else ""}
{f"Industry/Domain: {req.industry}" if req.industry else ""}
{f"Timeline: {req.timeline}" if req.timeline else ""}
{f"Budget: {req.budget}" if req.budget else ""}
{f"Client/Company: {req.client_name}" if req.client_name else ""}
{f"Additional Requirements: {req.extra_requirements}" if req.extra_requirements else ""}
""".strip()

    try:
        proposal_text = generate_proposal(enriched_input)
        return ProposalResponse(proposal_text=proposal_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download-pdf")
def download_pdf(req: ProposalResponse):
    if not req.proposal_text.strip():
        raise HTTPException(status_code=400, detail="Proposal text is required.")

    try:
        pdf_bytes = create_proposal_pdf(req.proposal_text)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=proposal.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))