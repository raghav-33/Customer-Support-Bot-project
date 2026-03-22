from src.state import AgentState
from langchain_core.messages import AIMessage

def human_agent_node(state: AgentState):
    
    handoff_message = "I am unable to resolve this request completely. I'm transferring you to a human agent who can better assist you. Please hold."
    
    return {""
    "generated_response": handoff_message,
    "messages": [AIMessage(content=handoff_message)]
    }