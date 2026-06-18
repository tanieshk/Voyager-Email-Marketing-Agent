# Voyager Email Marketing Agent

> Teleport Internship Assignment — Agentic Marketing Stack

<<<<<<< HEAD
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
=======
## Assignment Focus

**Primary Channel:** Email Marketing

This project was built around a single primary marketing channel: Email Marketing.

The email pipeline was implemented end-to-end, including research, copy generation, quality evaluation, self-healing revision, and responsive HTML rendering.

LinkedIn and WhatsApp outputs were added after the email pipeline was completed to validate architectural portability and demonstrate reuse of the same agent workflow across channels.

---

## What This Is

An agentic marketing system built for Voyager, an eSIM product for international travellers. Instead of one monolithic prompt, work is divided across four specialised agents: Research → Writer → Critic → Finalize. A self-healing loop catches bad output automatically and triggers rewrites before anything reaches a human.

Three output channels are supported. Email is the primary channel with full end-to-end engineering (MJML → responsive HTML). LinkedIn and WhatsApp are portability demonstrations — same graph, different prompts.

---

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph 0.2.74 |
| LLM | Groq `llama-3.3-70b` (free tier, swappable) |
| Email rendering | `mjml-python` (MJML → responsive HTML) |
| UI | Streamlit |
| API | FastAPI |

---
>>>>>>> 2adb4e1f469d053103bbc99bc2c026f9e94a4845

The system also includes LinkedIn post and WhatsApp message generators — same graph architecture, different prompt files — added as portability demonstrations after the email pipeline was complete.

<<<<<<< HEAD
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
=======
### 1. Clone and install

```bash
git clone <repo-url>
cd voyager-email-stack
pip install -r requirements.txt
```

### 2. Add your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

### 3. Run

**Streamlit UI (recommended):**
```bash
streamlit run streamlit_app.py
```

**FastAPI backend only:**
```bash
uvicorn app:app --reload
# POST to http://localhost:8000/generate
```

**CLI:**
```bash
python main.py
```

**Smoke test (no API key needed):**
```bash
python smoke_test.py
```

---

## Folder Structure
>>>>>>> 2adb4e1f469d053103bbc99bc2c026f9e94a4845

```
voyager-email-stack/
│
├── agents/
<<<<<<< HEAD
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
=======
│   ├── __init__.py          # Python package
│   ├── state.py             # Shared state (the baton passed between agents)
│   ├── prompts.py           # Personality and rules for each agent
│   ├── agents.py            # Agent node functions
│   ├── graph.py             # Email pipeline wiring
│   ├── linkedin_graph.py    # LinkedIn pipeline
│   └── whatsapp_graph.py    # WhatsApp pipeline
│
├── outputs/                 # Generated files land here
├── streamlit_app.py         # Visual UI
├── app.py                   # FastAPI backend
├── main.py                  # CLI runner
├── smoke_test.py            # Test without API key
├── requirements.txt
└── .env                     # API key (not committed)
>>>>>>> 2adb4e1f469d053103bbc99bc2c026f9e94a4845
```

---

<<<<<<< HEAD
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
=======
## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                   LangGraph Pipeline                    │
│                                                         │
│   ┌───────────────┐                                     │
│   │ Research Agent│  Builds brief, marks [VERIFY: ...]  │
│   └──────┬────────┘                                     │
│          │                                              │
│   ┌──────▼────────┐                                     │
│   │  Writer Agent │  Outputs structured JSON copy       │
│   └──────┬────────┘                                     │
│          │                                              │
│   ┌──────▼────────┐                                     │
│   │  Critic Agent │  Scores 4 dimensions, threshold 0.75│
│   └──────┬────────┘                                     │
│          │                                              │
│     ┌────▼─────┐                                        │
│     │ Pass?    │                                        │
│     └────┬─────┘                                        │
│          │                                              │
│    ✅ Yes │  ❌ No (max 2 retries)                      │
│          │         │                                    │
│   ┌──────▼──┐  ┌───▼──────────┐                        │
│   │Finalize │  │Writer Revision│ ← feedback injected   │
│   └──────┬──┘  └───┬──────────┘                        │
│          │         └──→ Critic Agent (re-score)         │
│   ┌──────▼──────┐                                       │
│   │  HTML Email │                                       │
│   └─────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## How It Works

### The Pipeline

```
START → research → writer → critic ──(fail, <2 revisions)──→ writer
                                 └──(pass OR max revisions)──→ finalize → END
```

### The Four Agents

**Research Agent** — Takes a scenario (e.g. "Pre-trip reminder for Japan") and produces a structured brief covering traveller pain points, relevant Voyager value props, and tone cues. Marks anything unverifiable with `[VERIFY: ...]`.

**Writer Agent** — Reads the research brief and produces structured JSON copy (subject, preheader, headline, body, CTA). On revision, it receives the previous draft plus specific critic feedback. For email, the JSON is compiled into MJML and rendered to responsive HTML.

**Critic Agent** — uses an LLM-as-a-Judge evaluation pattern. It scores the draft across four dimensions (subject strength, brand voice, CTA clarity, factual accuracy) and returns structured scores. These scores drive LangGraph routing decisions. Drafts below the threshold are automatically revised and re-evaluated, with a maximum of two revision loops.

| Dimension | What it catches |
|---|---|
| Subject line | Generic titles, missing specificity |
| Brand voice | Hype language, superlatives, ad-speak |
| CTA clarity | Weak or missing calls to action |
| Factual accuracy | Unmarked specific claims (prices, speeds, coverage %) |

**Finalize Node** — Deterministic (not an LLM call). Collects all `[VERIFY: ...]` flags, checks whether the draft passed, packages output, writes log.

### Self-Healing Loop

If the Critic scores below 0.75:
- Feedback goes back to the Writer as a revision prompt
- Writer revises (max 2 rounds)
- If still failing after 2 revisions, output is flagged for human review

---

## The Three Channels

### Email
Full pipeline. Structured JSON → MJML template → responsive HTML. Download button in UI. Critic rubric: subject, brand voice, CTA, accuracy.

### LinkedIn
Same graph, different prompts. Writer returns `{post_text, hook, hashtags}` (150–300 words). Critic scores hook strength and engagement. Renders as a LinkedIn card mockup.

### WhatsApp
Same graph, different prompts. Writer returns `{message, char_count}` (max 300 characters). Critic scores brevity. Renders as a WhatsApp bubble mockup.

### Critic Loop — Self-Healing Revision Workflow

![Critic Loop](docs/screenshots/critic_loop.png)

The Critic Agent evaluates generated content and can automatically trigger revisions when quality falls below the configured threshold. This self-healing loop is the core agentic behavior of the system.

---

## Screenshots

### Email — Agent Trace + Rendered Output

![Email Output](docs/screenshots/email_output.png)

### LinkedIn Post — Card Preview

![LinkedIn Output](docs/screenshots/linkedin_output.png)

### WhatsApp Message — Bubble Preview

![WhatsApp Output](docs/screenshots/whatsapp_output.png)

---

## Autonomy Boundary

The system acts fully autonomously through: research, writing, critic scoring, revision loop, and HTML rendering.

It stops and flags a human for:
- Any `[VERIFY: ...]` claim (prices, coverage numbers, carrier guarantees)
- Any draft that never passed the critic threshold after 2 revisions
- Before anything is actually sent

**The system never sends content.** Generation and delivery are intentionally decoupled.

---

## UI

The Streamlit UI (`streamlit_app.py`) shows:
- Live **agent trace** (what each agent did, in order)
- **Critic scores** per dimension with pass/fail badge
- **Rendered preview** — HTML email / LinkedIn card / WhatsApp bubble
- **Download button** for the final artifact
- **Human review flags** surfaced as warnings if any `[VERIFY: ...]` claims exist

---

## Scenarios

Pre-built scenarios available in the sidebar:
- Pre-trip reminder for Japan
- India tour

Custom scenario input is also supported — type any travel scenario and generate.

---

## Swapping the LLM

The model is configured in one place. To switch from Groq to OpenAI:

```python
# agents/agents.py
# Replace the Groq client initialisation with your preferred provider
```

The graph, state, and prompts are model-agnostic.

---

*Built by Tanieshk Yadav for the Teleport Internship Assignment.*
>>>>>>> 2adb4e1f469d053103bbc99bc2c026f9e94a4845
