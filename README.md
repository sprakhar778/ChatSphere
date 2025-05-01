# 💬 ChatSphere – Stateful, Tool-Augmented Conversational AI

[![LangGraph](https://img.shields.io/badge/built%20with-LangGraph-blueviolet)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**ChatSphere** is an intelligent conversational agent built with **LangGraph**, designed to deliver dynamic, tool-integrated, and memory-aware chat experiences. By combining the flexibility of graph-based orchestration with real-time search tools and LLMs, ChatSphere offers robust capabilities for information retrieval and contextual dialogue.

---

## 🌐 Why ChatSphere?

> LLMs are smart. But when you give them memory, tools, and structure—they become powerful.

ChatSphere enhances LLM interactions by:
- 🧠 Maintaining **stateful memory** across multiple messages
- 🌍 Using **web search tools** (Tavily, DuckDuckGo) for real-time context
- ⚙️ Leveraging **graph-based orchestration** for structured conversation flow
- 🔄 Trimming **chat history** for long conversations
- 🧪 Enabling experimentation with LLM agents and workflows

---

## 🧩 Core Architecture

ChatSphere is built using:

- **LangGraph** – to orchestrate the flow of conversation
- **LangChain** – to structure prompts and manage tools
- **TavilySearch / DuckDuckGoSearch** – for retrieving up-to-date content
- **Groq (LLaMA 4)** – as the backend LLM provider
- **Custom State Management** – for tracking chat and tool results

---
## ⚙️ Setup Instructions

Follow these steps to set up ChatSphere:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/ChatSphere.git
    cd ChatSphere
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the following:
    ```
    API_KEY=your_api_key_here
    SEARCH_ENGINE=your_search_engine_here
    ```

5. **Run the Application**:
    ```bash
    python main.py
    ```

6. **Access the Interface**:
    Open your browser and navigate to `http://localhost:8000`.

You're all set! 🎉