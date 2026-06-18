from typing import TypedDict, List, Dict, Any

class EmailState(TypedDict, total=False):
    scenario: str          # e.g. "pre-trip reminder for Japan"
    research_brief: str    # Research Agent output
    email_copy: dict       # Writer: subject, preheader, body_html, cta_text, cta_url
    mjml_source: str       # MJML markup
    html_output: str       # Rendered HTML
    critic_result: dict    # scores + feedback
    revision_count: int
    needs_human_review: List[str]
    pipeline_log: List[str]
