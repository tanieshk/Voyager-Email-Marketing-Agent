# Voyager Email Marketing Agent Stack

Multi-agent LangGraph pipeline that generates production-ready HTML marketing emails for Voyager eSIM.

## Architecture

```
research → writer → critic ──(fail, <2 revisions)──→ writer
                       └──(pass OR max revisions)──→ finalize
```

**Agents:**
1. **Research** — analyzes the email scenario, identifies pain points and messaging hooks
2. **Writer** — drafts email copy (subject, preheader, headline, body, CTA) as JSON, then renders to MJML → HTML
3. **Critic** (LLM-as-judge) — scores subject line, brand voice, CTA clarity, accuracy. Threshold 0.75. Triggers rewrite if below.
4. **Finalize** — packages output, flags anything needing human review before sending

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

## Run

```bash
# CLI
python main.py "Pre-trip reminder for Japan"

# Streamlit demo UI
streamlit run streamlit_app.py

# API
uvicorn app:app --reload
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"scenario":"last-minute eSIM offer"}'

# Smoke test (no API key needed)
python smoke_test.py
```

## Email Scenarios (built into Streamlit UI)
- Pre-trip reminder for Japan
- Last-minute eSIM offer — leaving tomorrow
- Post-landing activation guide
- Regional deal for Southeast Asia trip

## Human-in-the-loop
Any [VERIFY: ...] claims + emails that fail quality review are flagged in `needs_human_review` — must be checked before sending.
