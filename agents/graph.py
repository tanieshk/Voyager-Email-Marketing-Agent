from langgraph.graph import StateGraph, END
from agents.state import EmailState
from agents.agents import research_node, writer_node, critic_node, critic_router, finalize_node

def build_graph():
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
