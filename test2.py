from config import get_llm
from tools import explain_tool, quiz_tool, evaluate_tool, calculator_tool
from agent import create_agent
from db import save_interaction
import json

llm = get_llm()
USER_ID = "Ishita"

if __name__ == '__main__':
    # ---------------- LLM TEST ----------------
    print("\n--- LLM TEST ---")
    question_1 = "Tell me a joke"
    response = llm.invoke(question_1)
    print(response.content)

    # ✅ SAVE FIRST QUESTION
    save_interaction(USER_ID, question_1, response.content)
    print("Saved Q1 ✅")

    # ---------------- TOOL TESTS ----------------
    print("\n--- TOOL TESTS ---")
    print("Explain Tool:", explain_tool.invoke("Neural Networks"))
    print("Quiz Tool:", quiz_tool.invoke("Machine Learning"))
    print("Evaluate Tool:", evaluate_tool.invoke("ML is training models"))
    print("Calculator Tool:", calculator_tool.invoke("10 / 2 + 3"))

    # ---------------- AGENT TEST ----------------
    print("\n--- AGENT TEST ---")
    agent = create_agent()
    question_2 = "Explain Organic chemistry and then give me a quiz"

    # Initialize final output
    final_output = "PROCESSING..."

    # Save initial state
    save_interaction(USER_ID, question_2, final_output)
    print("Saved initial state ✅")

    try:
        print("Running agent...")
        # Modern LangGraph agent invocation
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Explain organic chemistry in simple terms, "
                            "then give a short quiz (3 questions max), "
                        ),
                    },
                    {"role": "user", "content": question_2},
                ]
            },
            verbose=True,
            max_iterations=3,
            agent="zero-shot-react-description",
            early_stopping_method="generate"
        )

        print("\nRAW RESULT:")
        print(result)

        # ✅ Extract final output safely
        messages = result.get("messages", [])
        if messages:
            # Last message content is the final answer
            final_output = messages[-1].content
        else:
            # fallback to string representation
            final_output = str(result)

    except Exception as e:
        print("Agent failed ❌")
        print(e)
        final_output = f"ERROR: {str(e)}"

    finally:
        print("\nSaving FINAL output to DB...")
        save_interaction(USER_ID, question_2, final_output)
        print("Saved final output ✅")

    # ---------------- DIRECT DB TEST ----------------
    print("\n--- DIRECT DB TEST ---")
    save_interaction(USER_ID, "Ishita", "test_response_2")
    print("Direct DB save worked ✅")