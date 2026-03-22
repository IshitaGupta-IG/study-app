from langchain.tools import tool
from config import get_llm

llm = get_llm()

@tool #decorator
def explain_tool(topic: str) -> str:
    """Explain a concept in simple terms for students""" #Docstring
    prompt = f"Explain {topic} in a simple way for a beginner student."
    return llm.invoke(prompt)

@tool
def quiz_tool(topic: str) -> str:
    """Generate 3 quiz questions for a topic"""
    prompt = f"Generate 3 quiz questions (with answers) on {topic}."
    return llm.invoke(prompt)

@tool
def evaluate_tool(answer: str) -> str:
    """Evaluate student's answer"""
    prompt = f"Evaluate this student answer and give feedback: {answer}"
    return llm.invoke(prompt)

@tool
def calculator_tool(expression: str) -> str:
    """Solve math expressions"""
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"