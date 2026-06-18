# Voyager Email Marketing Agent

> Teleport Internship Assignment — Agentic Marketing Stack

A multi-agent system that automates email marketing for **Voyager**, an eSIM for independent international travellers. The system takes a scenario as input and produces a publish-ready, responsive HTML email — without a human writing a single line of copy.

---

## What It Does

Given a scenario like `"Pre-trip reminder for Japan"`, four AI agents run in sequence:

```
Research → Writer → Critic ──(fail, ≤2 revisions)──→ Writer
                       └──(pass)──────────────────→ Finalize → HTML Email
```

1. **Research Agent** — builds a structured brief: traveller pain points, Voyager value props, tone cues. Marks anything unverifiable with `[VERIFY: ...]`.
2. **Writer Agent** — drafts a full email (subject, preheader, headline, body, CTA) as structured JSON, then renders it to MJML → responsive HTML.
3. **Critic Agent** — scores the draft across four dimensions (subject strength, brand voice, CTA clarity, factual accuracy). If the overall score falls below 0.75, it sends the draft back to the Writer with specific feedback. Loops up to 2 times.
4. **Finalize Node** — packages the output and surfaces all `[VERIFY: ...]` claims as a human review checklist. Nothing sends automatically.

The system also includes LinkedIn post and WhatsApp message generators — same graph architecture, different prompt files — added as portability demonstrations after the email pipeline was complete.

---

## Screenshots

### Email Pipeline — Agent trace, critic scores, rendered HTML email
![Email Demo](docs/screenshots/email_demo.png)

**India tour** scenario: Research → Writer → Critic (0.92 overall, Pass) → rendered HTML email with subject, preheader, CTA. No revisions needed on first pass.

### LinkedIn Pipeline — Post preview with card mockup
![LinkedIn Demo](docs/screenshots/linkedin_demo.png)

Same scenario, different channel. LinkedIn critic scores: Hook 0.8, Brand Voice 0.9, Engagement 0.7, Accuracy 1.0 — overall 0.85, Pass. Graph architecture unchanged, only prompts differ.

![LinkedIn Demo Full](docs/screenshots/linkedin_demo2.png)

Full LinkedIn card mockup rendered inline — profile header, post body, hashtags, like/comment/repost bar.

---

## Demo Scenarios (built into the UI)

- Pre-trip reminder for Japan
- Last-minute eSIM offer — leaving tomorrow
- Post-landing activation guide
- Regional deal for Southeast Asia trip
- Custom scenario (free text input)

---

## Stack

| Component | Technology |
|---|---|
| Agent orchestration | LangGraph 0.2.74 |
| LLM | Groq `llama-3.3-70b-versatile` (free tier) |
| Email rendering | `mjml-python` (MJML → responsive HTML) |
| Demo UI | Streamlit |
| API layer | FastAPI |
| Environment | Python 3.11 |

> **Note:** Groq is the default LLM (free, fast). To switch to OpenAI GPT-4o, replace `ChatGroq` with `ChatOpenAI` in `agents/agents.py` and set `OPENAI_API_KEY` instead.

---

## Setup

### Requirements
- Python 3.11 (not 3.12+, not 3.14 — package wheels require 3.11)
- A free [Groq API key](https://console.groq.com) — takes 2 minutes to get

### Install

```bash
# 1. Clone or unzip the project
cd voyager-email-stack

# 2. Create virtual environment with Python 3.11
py -3.11 -m venv venv          # Windows
python3.11 -m venv venv        # Mac/Linux

# 3. Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Add your API key
copy .env.example .env         # Windows
cp .env.example .env           # Mac/Linux
# Then open .env and set: GROQ_API_KEY=gsk_your_key_here
```

### Verify it works (no API key needed)

```bash
python smoke_test.py
```

Expected output:
```
[Research] Brief ready for: Pre-trip reminder for Japan
[Writer] Writing first draft
[Critic] Score: 0.5 | Pass: False
[Writer] Revising draft (revision 1)
[Critic] Score: 0.91 | Pass: True
[Pipeline] Done. Flagged: 0

SMOKE TEST PASSED
```

This confirms the graph wiring, self-healing critic loop, and JSON parsing all work correctly before spending any API credits.

---

## Running the System

### Streamlit UI (recommended for demo)

```bash
streamlit run streamlit_app.py
```

Opens in your browser. Select a scenario, click **Generate Email**, and watch the agents run live. The UI shows the agent trace, critic scores (color-coded), human review warnings, and a rendered HTML email preview. Tabs for LinkedIn and WhatsApp channels are also available.

### CLI

```bash
python main.py "Pre-trip reminder for Japan"
```

Prints the full agent trace, critic scores, and review flags to terminal. Saves the HTML email to `outputs/`.

### FastAPI (for integration)

```bash
uvicorn app:app --reload
```

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"scenario": "Pre-trip reminder for Japan"}'
```

---

## Project Structure

```
voyager-email-stack/
│
├── agents/
│   ├── state.py            # Shared state schema (TypedDict)
│   ├── prompts.py          # All agent system prompts + brand voice rules
│   ├── agents.py           # Email agent node functions
│   ├── graph.py            # LangGraph email pipeline
│   ├── linkedin_graph.py   # LinkedIn portability demo
│   └── whatsapp_graph.py   # WhatsApp portability demo
│
├── outputs/                # Generated HTML emails saved here
├── streamlit_app.py        # Demo UI (3-tab: Email, LinkedIn, WhatsApp)
├── app.py                  # FastAPI endpoint
├── main.py                 # CLI runner
├── smoke_test.py           # Mocked end-to-end test (no API key needed)
├── requirements.txt
└── .env.example
```

---

## Human-in-the-Loop Boundary

The system **never sends content automatically**. Generation and delivery are decoupled by design.

Before any output is sent, a human must review:
- Every `[VERIFY: ...]` flagged claim (prices, coverage %, carrier names — things the LLM cannot verify)
- Any email that did not pass the Critic's quality threshold after 2 revision attempts

These appear as explicit warnings in the Streamlit UI and in the CLI output.

---

## Output Example

Running the "Pre-trip reminder for Japan" scenario produces:

| Field | Example output |
|---|---|
| Subject | `Japan trip in 3 days? Your eSIM is ready` |
| Preheader | `Activate before you board — takes 60 seconds` |
| CTA | `Get Your Japan eSIM` |
| Critic score | 0.89 overall — Pass |
| Revisions | 1 |
| Flagged claims | 0 |
| Output file | `outputs/pre_trip_reminder_for_japan_email.html` |

---

## Limitations (honest)

- **No delivery layer** — the system generates emails but cannot send them. SendGrid/Mailgun integration would be the next step.
- **No user database** — one email per manual trigger. No segmentation, no audience logic.
- **English only** — no localisation.
- **Critic cannot verify ground truth** — it scores style and structure, not factual accuracy. The `[VERIFY: ...]` system surfaces claims, but a human must check them.

---

## Reasoning Document

See `voyager_reasoning.pdf` for the full design rationale: product positioning, channel choice, agent architecture decisions, autonomy boundaries, quality control layers, and scaling limitations.

---

*Built by Sonu (Tanieshk Ramesh Yadav) for the Teleport internship assignment.*