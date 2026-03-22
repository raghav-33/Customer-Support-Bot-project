from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.config import llm

# Pydantic Model
class ClassificationOutput(BaseModel):
    category:Literal["billing", "faq" , "technical", "general"] = Field(description="The exact category of the user's query.")
    is_angry: str = Field(description="Return the exact string 'True' ONLY if the user is using profanity, expressing extreme frustration, or explicitly demanding a human. Otherwise return the string 'False'.")


# llm 
llm_classifier = llm.with_structured_output(ClassificationOutput)

# prompt 
system_prompt = """You are an expert customer support triage agent.
Your job is to analyze the user's message and classify it into one of these specific categories:
- billing: Queries about invoices, payments, refunds, or subscription plans.
- faq: General company policy, operating hours, or basic non-technical questions.
- technical: Technical troubleshooting, bug reports, system errors, or API issues.
- general: Any standard conversational input (like "hello") or questions that do not fit the above.

You must also evaluate the user's emotional state. Flag 'is_angry' as True if the user is highly agitated or demands human escalation."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

# Combine into a single runnable chain
classification_chain = prompt | llm_classifier

# Node Function
def classify_query_node(state : AgentState):
    user_query = state["messages"][-1].content
    result = classification_chain.invoke({"question": user_query})

    # Convert the string "True"/"False" safely into a Python boolean
    is_angry_bool = (result.is_angry.lower() == "true")

    print(f"Decision -> Category: {result.category} | Angry: {is_angry_bool}")
    
    # Return the dictionary to update our AgentState
    return {
        "category": result.category,
        "is_angry": is_angry_bool
    }