from langchain_groq import ChatGroq
from langchain_classic.schema import HumanMessage


# router.py

def route_query(query: str):

    q = query.lower()

    # Sensitive intent
    if any(word in q for word in ["harassment", "abuse", "complaint"]):
        return "sensitive"

    # Comparison intent
    if "difference" in q or "compare" in q:
        return "comparison"

    # Calculation intent
    if any(word in q for word in ["calculate", "how much", "deduction"]):
        return "calculation"

    # Default = policy lookup
    return "policy_lookup"