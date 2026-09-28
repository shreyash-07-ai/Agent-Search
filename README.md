# 🔎 Agent-Search

An AI-powered research assistant built with Python, LangChain, Groq LLaMA 3.3, Streamlit, DuckDuckGo and Wikipedia.

Agent-Search takes a natural-language research question, decides which tools are useful, retrieves information, and presents a structured research summary.

## ✨ Features

- 🤖 Agentic research workflow with LangChain
- 🔍 DuckDuckGo web search for current/broad information
- 📚 Wikipedia lookup for background information
- 🧠 Groq LLaMA 3.3 70B for synthesis
- 📊 Structured research output
- ⬇️ Downloadable TXT research report
- 🧰 Displays tools used by the agent
- 🛡️ API keys kept outside the Git repository
- ☁️ Ready for Streamlit Community Cloud

## 🏗️ Architecture

~~~text
User Query
    ↓
Streamlit UI
    ↓
LangChain Agent
    ↓
Tool Selection: Web Search + Wikipedia
    ↓
Groq LLaMA 3.3 70B
    ↓
Structured Research Response
    ↓
Summary + Sources + Tools Used
    ↓
Downloadable Report
~~~

## 📁 Project Structure

~~~text
Agent-Search/
├── main.py
├── tools.py
├── requirements.txt
├── .gitignore
├── .env.example
├── .streamlit/
│   └── config.toml
└── README.md
~~~

## 🚀 Run Locally

### 1. Clone the repository

~~~bash
git clone https://github.com/shreyash-07-ai/Agent-Search.git
cd Agent-Search
~~~

### 2. Create a virtual environment

Windows:

~~~bash
python -m venv .venv
.venv\\Scripts\\activate
~~~

macOS/Linux:

~~~bash
python -m venv .venv
source .venv/bin/activate
~~~

### 3. Install dependencies

~~~bash
pip install -r requirements.txt
~~~

### 4. Configure your Groq API key

Copy .env.example to .env and add your key:

~~~env
GROQ_API_KEY=your_groq_api_key
~~~

Never commit .env.

### 5. Run Streamlit

~~~bash
streamlit run main.py
~~~

## ☁️ Deploy on Streamlit Community Cloud

1. Push the repository to GitHub.
2. Open Streamlit Community Cloud.
3. Select Create app.
4. Choose repository shreyash-07-ai/Agent-Search, branch main, and main file main.py.
5. Open Advanced settings → Secrets.
6. Add:

~~~toml
GROQ_API_KEY = "your_groq_api_key"
~~~

7. Deploy the app.

The API key is read from Streamlit Secrets and is not stored in GitHub.

## 🔐 Security

Do not commit API keys, .env files, or .streamlit/secrets.toml.

For Streamlit Community Cloud, configure secrets through the app settings.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq / LLaMA 3.3 70B
- DuckDuckGo Search via DDGS
- Wikipedia
- Pydantic
- python-dotenv

## 👨‍💻 Author

Shreyash Ashok Musmade

GitHub: https://github.com/shreyash-07-ai
