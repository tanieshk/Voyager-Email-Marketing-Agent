import json, os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from agents.state import EmailState
from agents.prompts import RESEARCH_PROMPT, WHATSAPP_WRITER_PROMPT, WHATSAPP_CRITIC_PROMPT

MAX_REVISIONS = 2

def _get_llm(temp=0.4):
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=temp)

def _strip(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"): t = t[4:]
    return t.strip()

def research_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    resp = _get_llm().invoke([
        SystemMessage(content=RESEARCH_PROMPT),
        HumanMessage(content=f"Scenario: {state['scenario']}")
    ])
    log.append(f"[Research] Brief ready for: {state['scenario']}")
    return {"research_brief": resp.content, "pipeline_log": log}

def writer_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    critic = state.get("critic_result")
    revision_count = state.get("revision_count", 0)

    user_msg = f"Scenario: {state['scenario']}\n\nResearch brief:\n{state['research_brief']}\n"
    if critic and not critic.get("pass", True):
        user_msg += f"\nREVISION FEEDBACK:\n{critic.get('feedback','')}\n\nPrevious message:\n{json.dumps(state.get('email_copy',{}), indent=2)}"
        revision_count += 1
        log.append(f"[WhatsApp Writer] Revising (revision {revision_count})")
    else:
        log.append("[WhatsApp Writer] Writing message")

    resp = _get_llm(0).invoke([
        SystemMessage(content=WHATSAPP_WRITER_PROMPT),
        HumanMessage(content=user_msg)
    ])
    try:
        copy = json.loads(_strip(resp.content))
        copy["char_count"] = len(copy.get("message", ""))
    except:
        msg = resp.content[:300]
        copy = {"message": msg, "char_count": len(msg)}

    return {"email_copy": copy, "revision_count": revision_count, "pipeline_log": log}

def critic_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    resp = _get_llm(0).invoke([
        SystemMessage(content=WHATSAPP_CRITIC_PROMPT),
        HumanMessage(content=f"Scenario: {state['scenario']}\n\nMessage:\n{json.dumps(state.get('email_copy',{}), indent=2)}")
    ])
    try:
        result = json.loads(_strip(resp.content))
    except:
        result = {"brevity_score":0,"brand_voice_score":0,"cta_score":0,
                  "accuracy_score":0,"overall_score":0,"pass":False,
                  "feedback":"Parse error","flagged_claims":[]}
    log.append(f"[WhatsApp Critic] Score: {result.get('overall_score')} | Pass: {result.get('pass')}")
    return {"critic_result": result, "pipeline_log": log}

def critic_router(state: EmailState) -> str:
    r = state.get("critic_result", {})
    if r.get("pass", False): return "finalize"
    if state.get("revision_count", 0) >= MAX_REVISIONS: return "finalize"
    return "writer"

def finalize_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    critic = state.get("critic_result", {})
    flagged = critic.get("flagged_claims", [])
    needs_review = list(flagged)
    if not critic.get("pass", True):
        needs_review.append("Message did not pass quality review — needs human check before sending.")
    log.append(f"[Pipeline] Done. Flagged: {len(needs_review)}")
    return {"needs_human_review": needs_review, "pipeline_log": log}

def build_whatsapp_graph():
    g = StateGraph(EmailState)
    g.add_node("research", research_node)
    g.add_node("writer", writer_node)
    g.add_node("critic", critic_node)
    g.add_node("finalize", finalize_node)
    g.set_entry_point("research")
    g.add_edge("research", "writer")
    g.add_edge("writer", "critic")
    g.add_conditional_edges("critic", critic_router, {"writer": "writer", "finalize": "finalize"})
    g.add_edge("finalize", END)
    return g.compile()
