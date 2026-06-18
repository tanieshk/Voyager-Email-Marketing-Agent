import os, json
from unittest.mock import patch
os.environ.setdefault("OPENAI_API_KEY", "sk-test")

from agents import agents as am
from agents.graph import build_graph

class FR:
    def __init__(self, c): self.content = c

responses = [
    FR("Pain point: no data on landing. Voyager: instant activation. Tone: reassuring."),
    FR(json.dumps({"subject":"Ready for Japan? Get your eSIM","preheader":"Activate in 60 seconds","headline":"Stay connected the moment you land","body":"Japan has excellent mobile coverage.\n\nWith Voyager, your eSIM is ready before you board.\n\nNo airport SIM queues. No roaming shock.","cta_text":"Get Your Japan eSIM","cta_url":"https://voyager.com/japan"})),
    FR(json.dumps({"subject_score":0.5,"brand_voice_score":0.5,"cta_score":0.5,"accuracy_score":0.5,"overall_score":0.5,"pass":False,"feedback":"- Subject too generic\n- Add urgency","flagged_claims":[]})),
    FR(json.dumps({"subject":"Japan trip in 3 days? Your eSIM is waiting","preheader":"Instant activation, no queues","headline":"Land in Japan. Connect instantly.","body":"Japan's mobile network is excellent.\n\nVoyager eSIM activates before you board — no airport queues, no SIM card hunting.\n\nTravel lighter. Stay connected.","cta_text":"Activate My Japan eSIM","cta_url":"https://voyager.com/japan"})),
    FR(json.dumps({"subject_score":0.9,"brand_voice_score":0.85,"cta_score":0.9,"accuracy_score":1.0,"overall_score":0.91,"pass":True,"feedback":"","flagged_claims":[]})),
]

idx = {"i": 0}
def fake_invoke(self, msgs):
    r = responses[idx["i"]]; idx["i"] += 1; return r

with patch.object(am.ChatOpenAI, "invoke", fake_invoke):
    state = build_graph().invoke({"scenario": "Pre-trip reminder for Japan", "revision_count": 0, "pipeline_log": []})

print("\n".join(state["pipeline_log"]))
assert state["critic_result"]["pass"] is True
assert state["revision_count"] == 1
assert state.get("html_output")
print("\nSMOKE TEST PASSED")
