from config import get_llm
from tools import explain_tool, quiz_tool, evaluate_tool, calculator_tool
from agent import create_agent

llm = get_llm()

if __name__ == '__main__':
    print("\n--- LLM TEST ---")
    response = llm.invoke("Tell me a joke")
    print(response.content)

    print("\n--- TOOL TESTS ---")
    print("Explain Tool:", explain_tool.invoke("Neural Networks"))
    print("Quiz Tool:", quiz_tool.invoke("Machine Learning"))
    print("Evaluate Tool:", evaluate_tool.invoke("ML is training models"))
    print("Calculator Tool:", calculator_tool.invoke("10 / 2 + 3"))

    print("\n--- AGENT TEST ---")
    agent = create_agent()

    user_input = "Explain AI and then give me a quiz and then tell me how many questions did you produce"


    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful teacher. Explain AI in simple terms, "
                        "then give a short quiz (3 questions max), "
                        "and finally count the questions. "
                        "Stop after completing these steps."
                    ),
                },
                {"role": "user", "content": user_input},
            ]
        }
    )

    print("\n--- AGENT OUTPUT ---")
    # Messages are Pydantic objects (SystemMessage, HumanMessage, AIMessage)
    # Access content via .content, role via __class__.__name__ for clarity
    for idx, msg in enumerate(result["messages"]):
        role_name = msg.__class__.__name__  # e.g., SystemMessage, HumanMessage, AIMessage
        print(f"{idx+1}. [{role_name}]: {msg.content}")

    # Final answer is the content of the last message
    final_answer = result["messages"][-1].content
    print("\n✅ Final Answer:\n", final_answer)