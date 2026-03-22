from src.state import AgentState
from src.config import llm
from src.config import embedding
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage

# Embedding model
embedding = embedding

# llm model
llm = llm

# loading Database
vectorstore = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Retriving document
retriever = vectorstore.as_retriever(
    search_type="similarity",  
    search_kwargs={"k": 2} 
)

# prompt
system_prompt = (
    "You are a helpful customer support assistant for an e-commerce company. "
    "Use the following pieces of retrieved context to answer the user's question. "
    "If the answer is not in the context, just say 'I don't have that information'. "
    "Do not make up answers. Keep your response clear and concise."
    "\n\nContext: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)


# Rag Node
def rag_node(state: AgentState):
    
    # Get the latest message from the graph state
    user_question = state["messages"][-1].content
    
    # Run your exact chain
    response = rag_chain.invoke({"input": user_question})
    
    # Return the answer to update the graph state
    return {
        "generated_response": response["answer"],
        "messages": [AIMessage(content=response["answer"])]
        }