from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import AgentState
from src.nodes.classifier import classify_query_node
from src.nodes.rag import rag_node
from src.nodes.direct_llm import llm_direct_node
from src.nodes.evaluator import resolution_evaluator_node
from src.nodes.human_agent import human_agent_node

memory = MemorySaver()

# Routing Function Node
def route_after_classification(state: AgentState):
    """Routes the query based on category and sentiment."""
    # If the user is extremely angry, bypass the AI and go straight to a human
    if state.get("is_angry"):
        return "human_agent_node"
    
    category = state.get("category")
    
    # Route to your unified Groq/FAISS RAG node for billing or FAQ
    if category in ["billing", "faq"]:
        return "rag_node"
    # Route to the direct LLM node for technical or general questions
    else:
        return "llm_direct_node"

# Evaluation Node 
def route_after_evaluation(state: AgentState):
    """Routes based on whether the AI successfully answered the question."""
    # If the evaluator marked it as unresolvable, send to human
    if state.get("is_resolved") is False:
        return "human_agent_node"
    
    # If resolved successfully, we are done!
    return "end"

# 1. Initialize the Graph with your AgentState schema
workflow = StateGraph(AgentState)

# 2. Add  nodes
workflow.add_node("classify_query_node", classify_query_node)
workflow.add_node("rag_node", rag_node)
workflow.add_node("llm_direct_node", llm_direct_node)
workflow.add_node("resolution_evaluator_node", resolution_evaluator_node)
workflow.add_node("human_agent_node", human_agent_node)

# 3. Add Edges


workflow.add_edge(START, "classify_query_node")
# Add the First Conditional Split (After Classification)
workflow.add_conditional_edges(
    "classify_query_node",
    route_after_classification,
    {
        "rag_node": "rag_node",
        "llm_direct_node": "llm_direct_node",
        "human_agent_node": "human_agent_node"
    }
)

# Connect the Generation Nodes to the Evaluator
# No matter which bot generated the answer, we must evaluate it
workflow.add_edge("rag_node", "resolution_evaluator_node")
workflow.add_edge("llm_direct_node", "resolution_evaluator_node")

#  Add the Second Conditional Split (After Evaluation)
workflow.add_conditional_edges(
    "resolution_evaluator_node",
    route_after_evaluation,
    {
        "end": END,
        "human_agent_node": "human_agent_node"
    }
)

#  Connect the Human Agent to END
workflow.add_edge("human_agent_node", END)

# 8. Compile the workflow
app = workflow.compile(checkpointer=memory)