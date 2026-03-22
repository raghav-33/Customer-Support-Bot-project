from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <-- NEW IMPORT
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import app as langgraph_app

# 1. Assuming your graph code is in a file named `graph.py`
# Import it as `langgraph_app` so it doesn't clash with FastAPI!
from graph import app as langgraph_app 

# 2. Initialize FastAPI
app = FastAPI(title="Customer Support AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all local connections
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    reply: str
    category: str

# 3. Define the Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        initial_state = {"messages": [HumanMessage(content=request.message)]}
        
        
        final_state = langgraph_app.invoke(initial_state, config=config)
        
        bot_reply = final_state.get("generated_response", "Error.")
        assigned_category = final_state.get("category", "unknown")
        
        return ChatResponse(reply=bot_reply, category=assigned_category)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

