from langchain_groq import ChatGroq
from langchain_classic.schema import HumanMessage

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

def rewrite_query(query):
    prompt = f"""
Rewrite the following HR query to improve retrieval from company policy documents.

Make it specific and include likely policy-related keywords.

Original Query:
{query}

Rewritten Query:
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()