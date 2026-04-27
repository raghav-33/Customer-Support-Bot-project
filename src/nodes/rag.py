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


def rag_node(state: AgentState):
    # Get the user's question
    user_question = state["messages"][-1].content
    
    #  retrieve documents from FAISS
    docs = retriever.invoke(user_question)
    
    # "stuffing" documents into a single string
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    formatted_messages = prompt.format_messages(
        context=context_text, 
        input=user_question
    )

    # llm calling
    response = llm.invoke(formatted_messages)
    
    # 5. Return the result
    return {
        "generated_response": response.content,
        "messages": [AIMessage(content=response.content)]
    }
