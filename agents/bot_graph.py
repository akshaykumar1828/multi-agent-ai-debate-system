from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from tools.search_tool import mock_searxng_search
import os
from dotenv import load_dotenv
from typing import TypedDict



load_dotenv()


# Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)





class GraphState(TypedDict):
    persona: str
    bot_id: str
    user_input: str   
    context: str
    output: str


# Node 2: Web Search
def web_search(state):
    query = state["user_input"]

    result = mock_searxng_search.invoke(query)

    return {"context": result}

# Node 3: Generate Post
def generate_post(state):
    persona = state["persona"]
    user_input = state["user_input"]
    context = state["context"]
    bot_id = state["bot_id"]

    prompt = f"""
    You are an AI debater with this personality:
    {persona}

    User statement:
    {user_input}

    Context:
    {context}

    IMPORTANT:
    You MUST respond ONLY to the user statement.
    Do NOT introduce unrelated topics (like AI, tech trends, etc.) unless directly relevant.

    Rules:
    - Stay strictly on the given statement
    - Continue the debate naturally
    - Max 40–50 words
    - Use 1–2 strong logical points
    - No storytelling, no generic phrases
    - No topic shifting
    - No assumptions

    Your response should directly challenge or support the statement logically.
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    
    output = response.content if response and response.content else "{}"

    return {"output": output}

# Build Graph
def create_graph():
    builder = StateGraph(GraphState)

    builder.add_node("web_search", web_search)
    builder.add_node("generate_post", generate_post)

    builder.set_entry_point("web_search")

    builder.add_edge("web_search", "generate_post")

    builder.set_finish_point("generate_post")

    return builder.compile()