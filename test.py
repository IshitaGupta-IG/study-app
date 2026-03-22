from config import get_llm
from tools import explain_tool, quiz_tool, evaluate_tool, calculator_tool

llm = get_llm()
if __name__ == '__main__':
    # LLM test
    response = llm.invoke("Tell me a joke")
    print(response.content)

    print("\n--- TOOL TESTS ---")

    print(explain_tool.invoke("Neural Networks"))
    print(quiz_tool.invoke("Machine Learning"))
    print(evaluate_tool.invoke("ML is training models"))
    print(calculator_tool.invoke("10 / 2 + 3"))
