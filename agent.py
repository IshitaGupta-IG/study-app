# agent.py
from langgraph.prebuilt import create_react_agent
from config import get_llm
from tools import explain_tool, quiz_tool, evaluate_tool, calculator_tool

def create_agent():
    llm = get_llm()

    tools = [
        explain_tool,
        quiz_tool,
        evaluate_tool,
        calculator_tool
    ]

    # Create the LangGraph agent (modern API)
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    return agent