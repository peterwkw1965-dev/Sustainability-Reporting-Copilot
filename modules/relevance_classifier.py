"""Rule-based sustainability topic and relevance classification."""

from __future__ import annotations


TOPIC_KEYWORDS = {
    "ISSB": ["issb", "ifrs s1", "ifrs s2", "climate disclosure"],
    "GRI": ["gri", "global reporting initiative"],
    "IMO": ["imo", "international maritime organization", "ghg strategy"],
    "EU ETS": ["eu ets", "emissions trading system", "shipping ets"],
    "FuelEU Maritime": ["fueleu", "fuel eu maritime"],
    "Carbon Markets": ["carbon market", "carbon price", "allowance", "offset"],
    "Climate Risk": ["climate risk", "physical risk", "transition risk", "scenario analysis"],
    "Net Zero": ["net zero", "net-zero", "science based targets", "sbti"],
    "Shipping Decarbonization": ["shipping", "maritime", "biofuel", "alternative fuel", "voyage optimization"],
    "Sustainable Finance": ["sustainable finance", "green bond", "sustainability-linked", "investor"],
    "Sustainability Assurance": ["assurance", "audit", "limited assurance", "reasonable assurance"],
}


def classify_topic(text: str) -> str:
    """Classify text into the requested sustainability topic list."""

    lower = (text or "").lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return topic
    return "General ESG"


def classify_relevance_to_tpc(text: str) -> str:
    """Explain why an item may matter to TPC Group."""

    lower = (text or "").lower()
    if any(term in lower for term in ["shipping", "maritime", "imo", "fueleu", "eu ets", "biofuel"]):
        return "High relevance: directly linked to maritime decarbonization, regulatory exposure, or shipping operations."
    if any(term in lower for term in ["issb", "ifrs s2", "gri", "assurance", "climate disclosure"]):
        return "High relevance: supports TPC Group's reporting journey from GRI to ISSB S1/S2 and assurance readiness."
    if any(term in lower for term in ["carbon", "net zero", "transition plan", "climate risk"]):
        return "Medium relevance: useful for net-zero roadmap, climate risk, or carbon cost planning."
    return "Monitor: may be relevant to general sustainability intelligence but needs management screening."


def suggest_action(text: str) -> str:
    """Suggest a practical management action based on the item content."""

    topic = classify_topic(text)
    if topic in {"ISSB", "GRI", "Sustainability Assurance"}:
        return "Review against TPC Group's disclosure gap list and update assurance evidence requirements if needed."
    if topic in {"IMO", "EU ETS", "FuelEU Maritime", "Shipping Decarbonization"}:
        return "Ask HSSE, operations, and finance to assess regulatory, cost, and transition plan implications."
    if topic in {"Carbon Markets", "Sustainable Finance"}:
        return "Monitor potential impact on carbon cost assumptions, financing, and Board reporting."
    if topic in {"Net Zero", "Climate Risk"}:
        return "Consider whether the item affects the net-zero roadmap, risk register, or scenario analysis assumptions."
    return "Keep on watchlist and review if it becomes material to TPC Group's reporting or strategy."
