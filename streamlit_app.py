import os, streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Voyager Marketing Stack",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Main background */
.stApp { background-color: #0f1117; }

/* Header banner */
.voyager-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border: 1px solid #0077ff33;
}
.voyager-header h1 {
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}
.voyager-header p {
    color: #8899bb;
    margin: 0.4rem 0 0 0;
    font-size: 1rem;
}

/* Pipeline flow */
.pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem;
    background: #1a1a2e;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.pipeline-step {
    background: #16213e;
    border: 1px solid #0077ff44;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #aabbdd;
    font-size: 0.85rem;
    font-weight: 600;
}
.pipeline-arrow { color: #0077ff; font-size: 1.2rem; }
.pipeline-step.active { background: #0077ff22; border-color: #0077ff; color: #ffffff; }

/* Score bars */
.score-bar-container { margin: 0.4rem 0; }
.score-label { color: #8899bb; font-size: 0.8rem; margin-bottom: 2px; }
.score-bar-bg { background: #1a1a2e; border-radius: 4px; height: 8px; width: 100%; }
.score-bar-fill { height: 8px; border-radius: 4px; transition: width 0.3s; }

/* Trace log */
.trace-line {
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    padding: 4px 12px;
    border-left: 3px solid #0077ff;
    margin: 3px 0;
    color: #aabbdd;
    background: #1a1a2e;
    border-radius: 0 4px 4px 0;
}

/* Cards */
.output-card {
    background: #1a1a2e;
    border: 1px solid #0077ff22;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.8rem 0;
}
.output-card h4 { color: #0077ff; margin: 0 0 0.5rem 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.output-card p { color: #ddeeff; margin: 0; font-size: 0.95rem; line-height: 1.5; }

/* Pass badge */
.badge-pass { background: #00ff8822; color: #00ff88; border: 1px solid #00ff8844; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.badge-fail { background: #ff444422; color: #ff4444; border: 1px solid #ff444444; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0f1117; border-right: 1px solid #1a1a2e; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #1a1a2e; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #8899bb; border-radius: 6px; }
.stTabs [aria-selected="true"] { background: #0077ff !important; color: white !important; }

button[kind="primary"] { background: #0077ff !important; border: none !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="voyager-header">
    <h1>✈️ Voyager Marketing Agent Stack</h1>
    <p>Voyager Email Marketing Agent

Primary Channel: Email
Extensions: LinkedIn · WhatsApp</p>
</div>
""", unsafe_allow_html=True)

# ── PIPELINE DIAGRAM ───────────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-flow">
    <div class="pipeline-step">🔍 Research Agent</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">✍️ Writer Agent</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">⚖️ Critic Agent</div>
    <div class="pipeline-arrow">⟲ self-heal</div>
    <div class="pipeline-step">✅ Finalize</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step active">📤 Output</div>
</div>
""", unsafe_allow_html=True)

# ── API KEY CHECK ──────────────────────────────────────────────────────────────
api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ Set GROQ_API_KEY or OPENAI_API_KEY in .env and restart.")
    st.stop()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    SCENARIOS = [
        "Pre-trip reminder for Japan",
        "Last-minute eSIM offer — leaving tomorrow",
        "Post-landing activation guide",
        "Regional deal for Southeast Asia trip",
    ]

    st.markdown("**Select Scenario**")
    scenario = st.selectbox("", SCENARIOS, label_visibility="collapsed")
    custom = st.text_input("✏️ Custom scenario", placeholder="e.g. Summer Europe trip")
    if custom: scenario = custom

    st.markdown("---")
    st.markdown(f"**Active scenario:**")
    st.info(scenario)

    st.markdown("---")
    st.markdown("**Model**")
    model_name = "llama-3.3-70b (Groq)" if os.environ.get("GROQ_API_KEY") else "gpt-4o (OpenAI)"
    st.caption(f"🤖 {model_name}")
    st.caption("🔄 Self-healing loop: max 2 revisions")
    st.caption("✅ Pass threshold: 0.75")

# ── HELPERS ────────────────────────────────────────────────────────────────────
def show_trace(log):
    st.markdown("**Agent Trace**")
    for line in log:
        st.markdown(f'<div class="trace-line">{line}</div>', unsafe_allow_html=True)

def score_color(val):
    if val >= 0.8: return "#00ff88"
    if val >= 0.6: return "#ffaa00"
    return "#ff4444"

def show_scores(c, keys):
    st.markdown("**Critic Scores**")
    cols = st.columns(len(keys) + 1)
    for col, key in zip(cols, keys):
        val = round(c.get(key, 0), 2)
        label = key.replace("_score","").replace("_"," ").title()
        color = score_color(val)
        col.markdown(f"""
        <div style="text-align:center">
            <div style="font-size:1.6rem;font-weight:700;color:{color}">{val}</div>
            <div style="font-size:0.72rem;color:#8899bb;margin-top:2px">{label}</div>
        </div>""", unsafe_allow_html=True)
    # overall + badge
    overall = round(c.get("overall_score", 0), 2)
    passed = c.get("pass", False)
    badge = '<span class="badge-pass">✓ PASS</span>' if passed else '<span class="badge-fail">✗ FAIL</span>'
    cols[-1].markdown(f"""
    <div style="text-align:center">
        <div style="font-size:1.6rem;font-weight:700;color:{score_color(overall)}">{overall}</div>
        <div style="font-size:0.72rem;color:#8899bb;margin-top:2px">Overall</div>
        <div style="margin-top:4px">{badge}</div>
    </div>""", unsafe_allow_html=True)

def show_review_flags(review):
    if review:
        st.markdown("**⚠️ Human Review Required Before Sending**")
        for item in review:
            st.warning(item)

def save_and_download(content, slug, ext, label):
    os.makedirs("outputs", exist_ok=True)
    path = f"outputs/{slug}.{ext}"
    with open(path, "w", encoding="utf-8") as f: f.write(content)
    st.download_button(f"⬇️ Download {label}", content,
                       file_name=f"{slug}.{ext}", mime="text/plain")

def get_slug(s): return "".join(c if c.isalnum() else "_" for c in s.lower())[:40]

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📧  Email", "💼  LinkedIn Post", "💬  WhatsApp Message"])

# ── EMAIL ──────────────────────────────────────────────────────────────────────
with tab1:
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.markdown("### Generate Email")
        st.caption("Full HTML marketing email with subject, preheader, body and CTA button.")
        if st.button("🚀 Generate Email", type="primary", key="email_btn", use_container_width=True):
            from agents.graph import build_graph
            with st.spinner("Agents running..."):
                state = build_graph().invoke({"scenario": scenario, "revision_count": 0, "pipeline_log": []})
            st.session_state["email_state"] = state

    if "email_state" in st.session_state:
        state = st.session_state["email_state"]
        with col_left:
            show_trace(state.get("pipeline_log", []))
            st.markdown("---")
            show_scores(state.get("critic_result", {}),
                        ["subject_score","brand_voice_score","cta_score","accuracy_score"])
            show_review_flags(state.get("needs_human_review", []))

            copy = state.get("email_copy", {})
            st.markdown(f"""
            <div class="output-card"><h4>Subject</h4><p>{copy.get('subject','')}</p></div>
            <div class="output-card"><h4>Preheader</h4><p>{copy.get('preheader','')}</p></div>
            <div class="output-card"><h4>CTA</h4><p>{copy.get('cta_text','')}</p></div>
            """, unsafe_allow_html=True)
            save_and_download(state.get("html_output",""), get_slug(scenario)+"_email", "html", "HTML Email")

        with col_right:
            st.markdown("### Rendered Email Preview")
            st.components.v1.html(state.get("html_output",""), height=620, scrolling=True)

# ── LINKEDIN ───────────────────────────────────────────────────────────────────
with tab2:
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.markdown("### Generate LinkedIn Post")
        st.caption("150-300 word post with hook, body, and hashtags.")
        if st.button("🚀 Generate LinkedIn Post", type="primary", key="li_btn", use_container_width=True):
            from agents.linkedin_graph import build_linkedin_graph
            with st.spinner("Agents running..."):
                state = build_linkedin_graph().invoke({"scenario": scenario, "revision_count": 0, "pipeline_log": []})
            st.session_state["li_state"] = state

    if "li_state" in st.session_state:
        state = st.session_state["li_state"]
        with col_left:
            show_trace(state.get("pipeline_log", []))
            st.markdown("---")
            show_scores(state.get("critic_result", {}),
                        ["hook_score","brand_voice_score","engagement_score","accuracy_score"])
            show_review_flags(state.get("needs_human_review", []))
            copy = state.get("email_copy", {})
            st.markdown(f"""
            <div class="output-card"><h4>Hook (First Line)</h4><p>{copy.get('hook','')}</p></div>
            <div class="output-card"><h4>Hashtags</h4><p>{' '.join(copy.get('hashtags',[]))}</p></div>
            """, unsafe_allow_html=True)
            save_and_download(copy.get("post_text",""), get_slug(scenario)+"_linkedin", "txt", "LinkedIn Post")

        with col_right:
            st.markdown("### LinkedIn Post Preview")
            post_text = state.get("email_copy", {}).get("post_text", "")
            # LinkedIn card mockup
            st.components.v1.html(f"""
            <div style="font-family:Arial,sans-serif;background:#f3f2ef;padding:20px;border-radius:12px;">
              <div style="background:white;border-radius:8px;padding:16px;
                          box-shadow:0 1px 3px rgba(0,0,0,0.12);max-width:560px;margin:auto;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                  <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#1a1a2e,#0077ff);
                              display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:18px;">V</div>
                  <div>
                    <div style="font-weight:700;font-size:14px;color:#1a1a2e">Voyager eSIM</div>
                    <div style="font-size:12px;color:#666">Travel Technology · Just now</div>
                  </div>
                </div>
                <div style="font-size:14px;color:#1a1a2e;line-height:1.6;white-space:pre-wrap">{post_text}</div>
                <div style="margin-top:12px;padding-top:12px;border-top:1px solid #eee;
                            display:flex;gap:16px;color:#666;font-size:13px;">
                  <span>👍 Like</span><span>💬 Comment</span><span>🔁 Repost</span><span>📤 Send</span>
                </div>
              </div>
            </div>""", height=500, scrolling=True)

# ── WHATSAPP ───────────────────────────────────────────────────────────────────
with tab3:
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.markdown("### Generate WhatsApp Message")
        st.caption("Max 300 chars. Conversational, emoji-friendly broadcast message.")
        if st.button("🚀 Generate WhatsApp Message", type="primary", key="wa_btn", use_container_width=True):
            from agents.whatsapp_graph import build_whatsapp_graph
            with st.spinner("Agents running..."):
                state = build_whatsapp_graph().invoke({"scenario": scenario, "revision_count": 0, "pipeline_log": []})
            st.session_state["wa_state"] = state

    if "wa_state" in st.session_state:
        state = st.session_state["wa_state"]
        with col_left:
            show_trace(state.get("pipeline_log", []))
            st.markdown("---")
            show_scores(state.get("critic_result", {}),
                        ["brevity_score","brand_voice_score","cta_score","accuracy_score"])
            show_review_flags(state.get("needs_human_review", []))
            copy = state.get("email_copy", {})
            msg = copy.get("message","")
            char_count = copy.get("char_count", len(msg))
            color = "#00ff88" if char_count <= 300 else "#ff4444"
            st.markdown(f'<p style="color:{color};font-size:0.85rem">📏 {char_count}/300 characters</p>', unsafe_allow_html=True)
            save_and_download(msg, get_slug(scenario)+"_whatsapp", "txt", "WhatsApp Message")

        with col_right:
            st.markdown("### WhatsApp Preview")
            msg = state.get("email_copy", {}).get("message", "")
            st.components.v1.html(f"""
            <div style="font-family:Arial,sans-serif;background:#111b21;
                        min-height:400px;border-radius:12px;padding:20px;">
              <!-- header bar -->
              <div style="display:flex;align-items:center;gap:10px;
                          background:#202c33;padding:12px 16px;border-radius:8px;margin-bottom:20px;">
                <div style="width:40px;height:40px;border-radius:50%;
                            background:linear-gradient(135deg,#1a1a2e,#0077ff);
                            display:flex;align-items:center;justify-content:center;
                            color:white;font-weight:bold;">V</div>
                <div>
                  <div style="color:white;font-weight:600;font-size:14px">Voyager eSIM</div>
                  <div style="color:#8696a0;font-size:12px">Business Account</div>
                </div>
              </div>
              <!-- message bubble -->
              <div style="display:flex;justify-content:flex-end;padding:0 8px;">
                <div style="background:#005c4b;color:#e9edef;padding:10px 14px;
                            border-radius:12px 2px 12px 12px;max-width:75%;
                            font-size:14px;line-height:1.5;
                            box-shadow:0 1px 2px rgba(0,0,0,0.3);">
                  {msg}
                  <div style="text-align:right;font-size:11px;color:#8696a0;margin-top:4px">
                    10:30 AM ✓✓
                  </div>
                </div>
              </div>
            </div>""", height=400)