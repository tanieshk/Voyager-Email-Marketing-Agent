import argparse, os, sys
from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    print("ERROR: Set GROQ_API_KEY in .env"); sys.exit(1)

from agents.graph import build_graph

def run(scenario: str):
    app = build_graph()
    print(f"\nRunning Voyager email pipeline for: '{scenario}'\n")
    state = app.invoke({"scenario": scenario, "revision_count": 0, "pipeline_log": []})

    print("=== Pipeline Log ===")
    for line in state.get("pipeline_log", []): print(line)

    print("\n=== Critic Scores ===")
    c = state.get("critic_result", {})
    for k in ["subject_score","brand_voice_score","cta_score","accuracy_score","overall_score"]:
        print(f"  {k}: {c.get(k)}")
    print(f"  pass: {c.get('pass')}")

    print("\n=== Email Copy ===")
    copy = state.get("email_copy", {})
    print(f"  Subject: {copy.get('subject')}")
    print(f"  Preheader: {copy.get('preheader')}")
    print(f"  CTA: {copy.get('cta_text')}")

    review = state.get("needs_human_review", [])
    if review:
        print("\n=== Human Review Required ===")
        for item in review: print(f"  - {item}")

    slug = "".join(c if c.isalnum() else "_" for c in scenario.lower())[:40]
    os.makedirs("outputs", exist_ok=True)
    html_path = f"outputs/{slug}.html"
    with open(html_path, "w") as f:
        f.write(state.get("html_output", ""))
    print(f"\nHTML email saved to: {html_path}")
    return state

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("scenario", help="e.g. 'pre-trip reminder for Japan'")
    args = p.parse_args()
    run(args.scenario)
