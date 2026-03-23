from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from db import save_interaction

app = FastAPI()

# Initialize agent once
agent = create_agent()

class Query(BaseModel):
    user_id: str
    question: str

@app.get("/")
def home():
    return {"message": "AI Study Agent is running"}

@app.post("/study")
async def study(query: Query):
    messages = [{"role": "user", "content": query.question}]

    # Invoke agent
    result = agent.invoke(
        {"messages": messages},
        verbose=True,
        max_iterations=3
    )

    result_text = getattr(result, "content", str(result))

    # Save to DynamoDB
    save_interaction(
        query.user_id,
        query.question,
        result_text
    )

    # Return plain string
    return {"response": result_text}