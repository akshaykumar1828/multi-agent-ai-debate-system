from langchain.tools import tool

@tool
def mock_searxng_search(query: str) -> str:
    """Returns dynamic mock news based on query"""

    return f"""
    Latest news about {query}:
    - AI adoption is increasing globally
    - Markets are reacting to tech innovations
    - Experts predict major changes in the next 5 years
    """