Here is the fully fixed, clean version. I removed the markdown hyperlink brackets inside the code block that caused the formatting glitch in your screenshot. 

Click the **"Copy"** button in the top-right corner of the block below and paste it directly into your GitHub `README.md` file!

```markdown
# 🤖 ResolveAI: Customer Support AI Agent

ResolveAI is a production-ready, full-stack customer support AI built with a multi-agent LangGraph architecture. It features a Retrieval-Augmented Generation (RAG) pipeline to accurately answer questions based on company policies, maintains conversational memory across multiple turns, and is served via a high-performance FastAPI backend to a modern, glassmorphism-styled web widget.

## ✨ Key Features

* **Multi-Agent Routing:** Uses LangGraph to dynamically classify user intents and route queries to specialized agents (e.g., General FAQ, Technical Support, or Billing).
* **RAG Pipeline:** Integrates a FAISS vector database and HuggingFace embeddings to search and retrieve accurate information from unstructured company documents (like refund policies and FAQs), drastically reducing LLM hallucinations.
* **Stateful Memory:** Implements LangChain thread IDs and check-pointing to remember conversation history, allowing users to ask complex, multi-turn follow-up questions.
* **Custom Frontend Widget:** A fully responsive, modern chat widget built with pure HTML, CSS, and Vanilla JavaScript, featuring real-time typing indicators and asynchronous API fetching.
* **FastAPI Backend:** A robust REST API layer handling CORS middleware, Pydantic schema validation, and error handling.

## 🏗️ System Architecture

1. **Frontend (HTML/CSS/JS):** A lightweight client that securely sends POST requests to the backend and dynamically renders chat bubbles.
2. **Backend API (FastAPI):** Receives user input, manages session IDs, and acts as the bridge between the client and the LangGraph AI environment.
3. **AI Layer (LangGraph & LangChain):** Orchestrates the LLM (Groq/Llama-3). It decides whether to query the vector database or use standard conversational logic.
4. **Data Layer (FAISS):** Stores chunked vector embeddings of company text documents for semantic search.

## 💻 Tech Stack

* **Frontend:** Vanilla JavaScript, HTML5, CSS3 (Glassmorphism UI)
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **AI & Orchestration:** LangGraph, LangChain, Groq API (Llama models)
* **Vector DB & Embeddings:** FAISS, HuggingFace (`all-MiniLM-L6-v2`)

## 🚀 Getting Started

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/resolve-ai-support-bot.git](https://github.com/your-username/resolve-ai-support-bot.git)
cd resolve-ai-support-bot
```

### 2. Backend & AI Setup
Open a terminal and set up your Python environment.

```bash
# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install fastapi uvicorn langchain langgraph langchain-community langchain-huggingface pydantic faiss-cpu sentence-transformers langchain-groq

# Create a .env file and add your API Key
echo GROQ_API_KEY=your_api_key_here > .env
```

### 3. Initialize the Vector Database
Before starting the server, you need to convert the text files into vector embeddings.

1. Ensure your text files (e.g., `faq.txt`, `refundpolicy.txt`) are inside the `data/` folder.
2. Run the ingestion script:

```bash
python ingest.py
```
*You should see a success message indicating the FAISS database was built and saved.*

### 4. Start the Application
Start the FastAPI backend server:

```bash
uvicorn main:app --reload
```
*The API will be running at `http://127.0.0.1:8000`*

To view the UI, simply double-click the `index.html` file in your file explorer to open it in your web browser. 

## 🎮 How to Use

1. Click the floating blue chat bubble in the bottom right corner of the `index.html` page.
2. Ask a policy-specific question, such as: *"What is your refund policy?"* or *"Do you offer a twice money pay guarantee?"*
3. The AI will embed your query, search the FAISS database, and return a highly accurate answer based strictly on your company files.
4. Ask a follow-up question (e.g., *"How long does that take?"*) to test the system's stateful memory!

## 🛡️ License
This project is open-source and available under the MIT License.
```
