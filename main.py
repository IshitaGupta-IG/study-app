from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from db import save_interaction
from tools import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

agent = create_agent()

class Query(BaseModel):
    user_id: str
    question: str

@app.get("/")
def home():
    return {"message": "AI Study Agent is running"}

@app.post("/study")
async def study(query: Query):
    # -----------------------
    # Prepare messages for the agent
    # -----------------------
    messages = [{"role": "user", "content": query.question}]

    try:
        result = agent.invoke({
            "messages": messages,
            "agent_scratchpad": []      # 👈 scratch pad for intermediate reasoning
        })

        print("RAW RESULT:", result)

        # Extract text safely
        response = result.get("output", str(result))

    except Exception as e:
        print("Agent failed ❌", e)

        # Fallback tools
        explanation = explain_tool.invoke(query.question)
        quiz = quiz_tool.invoke(query.question)

        response = f"{explanation}\n\n{quiz}"

    # Save interaction
    try:
        save_interaction(query.user_id, query.question, response)
    except Exception as db_err:
        print("Failed to save to DB ❌", db_err)

    return {"response": response}

app = FastAPI()

# ✅ ADD THIS BLOCK
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],   # allow all (dev only)
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
