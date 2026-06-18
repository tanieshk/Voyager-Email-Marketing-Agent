import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from agents.graph import build_graph

app = FastAPI(title="Voyager Email Agent Stack")
graph_app = build_graph()

class GenerateRequest(BaseModel):
    scenario: str

@app.get("/")
def root(): return {"status": "ok"}

@app.post("/generate")
def generate(req: GenerateRequest):
    state = graph_app.invoke({"scenario": req.scenario, "revision_count": 0, "pipeline_log": []})
    return {
        "scenario": req.scenario,
        "subject": state.get("email_copy", {}).get("subject"),
        "html_output": state.get("html_output"),
        "critic_result": state.get("critic_result"),
        "needs_human_review": state.get("needs_human_review"),
        "pipeline_log": state.get("pipeline_log"),
    }
