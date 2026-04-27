from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser 
from src.config import llm
from src.state import AgentState

direct_llm = llm

direct_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a highly skilled technical and general support agent to resolve technical problem in any Purchased product. "
        "Answer the user's question clearly and concisely. "
        "If they are just saying hello, greet them politely. "
        "Do not make up specific company policies."
    )),
    MessagesPlaceholder(variable_name="chat_history") 
])

# By adding StrOutputParser() to the end, the chain will NEVER return an AIMessage object again.
direct_chain = direct_prompt | direct_llm | StrOutputParser()

def llm_direct_node(state: AgentState): 
    print("---RUNNING DIRECT LLM NODE---")
    try:
        response_string = direct_chain.invoke({"chat_history": state["messages"]})
        
        return {
            "generated_response": response_string,
            "messages": [AIMessage(content=response_string)]
        }
        
    except Exception as e:
        print(f"Direct LLM Error: {e}")
        fallback_msg = "I'm experiencing a minor network hiccup. Could you please rephrase your question?"
        
        return {
            "generated_response": fallback_msg,
            "messages": [AIMessage(content=fallback_msg)]
        }
