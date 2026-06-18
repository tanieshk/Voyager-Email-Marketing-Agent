import json, os
try:
  from langchain_groq import ChatGroq as LLMClass
except ImportError:
  from langchain_openai import ChatOpenAI as LLMClass
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import EmailState
from agents.prompts import RESEARCH_PROMPT, WRITER_PROMPT, CRITIC_PROMPT

MAX_REVISIONS = 2
llm = LLMClass(model="llama-3.3-70b-versatile" if "ChatGroq" in str(LLMClass) else "gpt-4o", temperature=0.4)
llm_json = LLMClass(model="llama-3.3-70b-versatile" if "ChatGroq" in str(LLMClass) else "gpt-4o", temperature=0)

def _strip(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"): t = t[4:]
    return t.strip()

def _build_mjml(copy: dict) -> str:
    return f"""<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
    <mj-preview>{copy.get('preheader','')}</mj-preview>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <mj-section background-color="#1a1a2e" padding="20px">
      <mj-column>
        <mj-text color="#ffffff" font-size="24px" font-weight="bold" align="center">
          Voyager eSIM
        </mj-text>
      </mj-column>
    </mj-section>
    <mj-section background-color="#ffffff" padding="30px">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#1a1a2e">
          {copy.get('headline','')}
        </mj-text>
        <mj-text font-size="15px" color="#444444" line-height="1.6">
          {copy.get('body','').replace(chr(10), '<br/>')}
        </mj-text>
        <mj-button background-color="#0077ff" color="#ffffff"
          href="{copy.get('cta_url','https://voyager.com/plans')}"
          font-size="16px" border-radius="4px" padding="15px 30px">
          {copy.get('cta_text','Get Your eSIM')}
        </mj-button>
      </mj-column>
    </mj-section>
    <mj-section background-color="#f4f4f4" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#999999" align="center">
          Voyager eSIM · Stay connected everywhere · Unsubscribe
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>"""

def _render_html(mjml_src: str) -> str:
    try:
        from mjml import mjml2html
        result = mjml2html(mjml_src)
        return result.html if hasattr(result, 'html') else str(result)
    except Exception:
        return f"<html><body>{mjml_src}</body></html>"

# --- Nodes ---

def research_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    resp = llm.invoke([
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
        user_msg += f"\nREVISION FEEDBACK:\n{critic.get('feedback','')}\n\nPrevious copy:\n{json.dumps(state.get('email_copy',{}), indent=2)}"
        revision_count += 1
        log.append(f"[Writer] Revising draft (revision {revision_count})")
    else:
        log.append("[Writer] Writing first draft")

    resp = llm_json.invoke([
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=user_msg)
    ])
    try:
        copy = json.loads(_strip(resp.content))
    except Exception:
        copy = {"subject": "Travel smarter with Voyager", "preheader": "Your eSIM, ready to go.",
                "headline": "Stay connected on your trip", "body": resp.content,
                "cta_text": "Get Your eSIM", "cta_url": "https://voyager.com/plans"}

    mjml = _build_mjml(copy)
    html = _render_html(mjml)
    return {"email_copy": copy, "mjml_source": mjml, "html_output": html,
            "revision_count": revision_count, "pipeline_log": log}

def critic_node(state: EmailState) -> dict:
    log = state.get("pipeline_log", [])
    resp = llm_json.invoke([
        SystemMessage(content=CRITIC_PROMPT),
        HumanMessage(content=f"Scenario: {state['scenario']}\n\nEmail copy:\n{json.dumps(state.get('email_copy',{}), indent=2)}")
    ])
    try:
        result = json.loads(_strip(resp.content))
    except Exception:
        result = {"subject_score":0,"brand_voice_score":0,"cta_score":0,
                  "accuracy_score":0,"overall_score":0,"pass":False,
                  "feedback":"Could not parse critic output. Regenerate.","flagged_claims":[]}
    log.append(f"[Critic] Score: {result.get('overall_score')} | Pass: {result.get('pass')}")
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
        needs_review.append("Email did not pass quality review — needs human edit before sending.")
    log.append(f"[Pipeline] Done. Flagged items: {len(needs_review)}")
    return {"needs_human_review": needs_review, "pipeline_log": log}
