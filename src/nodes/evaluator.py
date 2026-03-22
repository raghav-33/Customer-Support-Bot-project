# Imports
from pydantic import BaseModel,Field
from typing import List,Annotated
from src.config import llm
from src.state import AgentState
from langchain_core.prompts import ChatPromptTemplate

# Pydantic Schema
class EvaluationOutput(BaseModel):
    is_resolved: str = Field( description="Return the exact string 'True' if the response answers the question successfully. Return the string 'False' if the response says 'I don't have that information' or is completely unhelpful.")

# LLM
evaluator_llm = llm.with_structured_output(EvaluationOutput)

# Prompt
evaluator_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a quality assurance bot. Did the 'Generated Response' "
        "successfully answer the 'User Query'? Respond carefully."
    )),
    ("human", "User Query: {query}\n\nGenerated Response: {response}")
])

eval_chain = evaluator_prompt | evaluator_llm

#  The Evaluator  Node Function
def resolution_evaluator_node(state: AgentState):

    user_query = state["messages"][-1].content
    draft_response = state["generated_response"]
    result = eval_chain.invoke({"query": user_query, "response": draft_response})

    # Convert the string "True"/"False" safely into a Python boolean
    is_resolved_bool = (result.is_resolved.lower() == "true")
    
    print(f"Is Resolved? {is_resolved_bool}")
    
    # Update the boolean flag in the state
    return {"is_resolved": is_resolved_bool}
