# Agent-Search
Agentic-AI Project

# 🧠 AI-Powered Research Assistant

An AI-powered research assistant built with Python, LangChain, and Groq LLaMA-3.  
This agent can:
- 🔍 Search the web using DuckDuckGo
- 📖 Fetch summaries from Wikipedia
- 💾 Save research results into structured text reports

🚀 Features
- Uses Groq LLaMA-3 (70B) model for research-quality responses
- Integrates with DuckDuckGo & Wikipedia API
- Saves structured output (topic, summary, sources, tools used) into timestamped `.txt` files
- Modular tool system (`search_tool`, `wiki_tool`, `save_tool`)

🛠️ Tech Stack
- Python, LangChain
- Groq API (LLaMA-3)
- DuckDuckGo Search API, Wikipedia API
- Pydantic, dotenv


📌 Steps are as follows:-

1. Install dependencies:
      pip install -r requirements.txt
2. Add your API key in .env:
      GROQ_API_KEY=your_api_key_here
3. Run the agent:
      python main.py


📌 Example Output:-

--- Research Output ---
Timestamp: 2025-08-27 19:45:00

Topic: Artificial Intelligence

Summary:
Artificial Intelligence (AI) is the simulation of human intelligence processes by machines...

Sources: Wikipedia, DuckDuckGo
Tools Used: wiki_tool, search_tool
