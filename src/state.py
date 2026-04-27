from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # Mantaing Conversation history
    category: str # [billing,Faq,Genral,Technical]
    is_angry: bool # Checking User Behaviour (Angry or not)
    is_resolved: bool # Final Evalution Query got Resolved or Not
    generated_response: str # Generated Response to user Query
