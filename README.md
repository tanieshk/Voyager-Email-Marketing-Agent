# Voyager Email Marketing Agent

> Teleport Internship Assignment — Agentic Marketing Stack

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

## Setup

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

```
voyager-email-stack/
│
├── agents/
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
```

---

## Architecture

```text
Research Agent
      ↓
Writer Agent
      ↓
Critic Agent
      ↓
(pass)
      ↓
Finalize
      ↓
HTML Email

(fail)
      ↓
Writer Revision
      ↓
Critic Agent
      ↓
(max 2 loops)
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
