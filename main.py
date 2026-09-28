import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from tools import search_tool, wiki_tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str = Field(description="The main research topic.")
    summary: str = Field(description="A concise but useful research summary.")
    sources: list[str] = Field(default_factory=list)
    tools_used: list[str] = Field(default_factory=list)


def get_secret(name: str) -> str:
    """Read a secret from Streamlit secrets first, then environment variables."""
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, "")


def build_agent():
    api_key = get_secret("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured. Add it to Streamlit Secrets "
            "or your local .env file."
        )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=api_key,
        max_retries=2,
    )

    system_prompt = """You are Agent-Search, an AI research assistant.

Research the user's question using the available tools when current or factual
information is needed. Prefer web search for current information and Wikipedia
for background/context. Synthesize the retrieved information into a clear,
accurate answer.

Return ONLY valid JSON with this exact shape:
{
  "topic": "string",
  "summary": "string",
  "sources": ["source/tool names or useful source references"],
  "tools_used": ["search", "wikipedia"]
}

Do not use markdown code fences around the JSON.
Do not invent sources. If a tool is not used, do not list it.
"""

    return create_agent(
        model=llm,
        tools=[search_tool, wiki_tool],
        system_prompt=system_prompt,
    )


def parse_response(result: dict, fallback_topic: str) -> ResearchResponse:
    messages = result.get("messages", [])
    content = ""

    for message in reversed(messages):
        if getattr(message, "type", "") == "ai":
            content = getattr(message, "content", "")
            if content:
                break

    if isinstance(content, list):
        content = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    content = str(content).strip()

    try:
        return ResearchResponse.model_validate_json(content)
    except Exception:
        return ResearchResponse(
            topic=fallback_topic,
            summary=content,
            sources=["Agent response"],
            tools_used=["search / wikipedia (if selected by the agent)"],
        )


def make_report(response: ResearchResponse) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        "--- Agent-Search Research Report ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"Topic: {response.topic}\n\n"
        f"Summary:\n{response.summary}\n\n"
        f"Sources: {', '.join(response.sources) or 'Not specified'}\n"
        f"Tools Used: {', '.join(response.tools_used) or 'Not specified'}\n"
    )


st.set_page_config(
    page_title="Agent-Search | AI Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔎 Agent-Search")
st.caption("AI-powered research assistant using LangChain, Groq, DuckDuckGo and Wikipedia.")

with st.sidebar:
    st.header("About Agent-Search")
    st.write(
        "Ask a research question and let the agent decide when to use web search "
        "or Wikipedia before synthesizing the final response."
    )

    st.divider()
    st.subheader("Tools")
    st.markdown("- 🔍 DuckDuckGo web search")
    st.markdown("- 📚 Wikipedia lookup")
    st.markdown("- 🤖 Groq LLaMA 3.3 70B")

    st.divider()
    st.subheader("Deployment")
    st.caption("Designed for Streamlit Community Cloud.")
    st.caption("API keys are loaded from Streamlit Secrets and are never stored in the repository.")

    if st.button("Clear research", use_container_width=True):
        st.session_state.pop("last_response", None)
        st.session_state.pop("last_query", None)
        st.rerun()

query = st.text_area(
    "What would you like to research?",
    placeholder="Example: How has generative AI changed software development?",
    height=120,
)

col1, col2 = st.columns([1, 5])
with col1:
    research_clicked = st.button("🚀 Research", type="primary", use_container_width=True)

if research_clicked:
    if not query.strip():
        st.warning("Please enter a research question.")
    else:
        with st.status("Researching...", expanded=True) as status:
            try:
                st.write("Initializing Agent-Search...")
                agent = build_agent()

                st.write("Selecting the most relevant research tools...")
                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": query.strip(),
                            }
                        ]
                    }
                )

                st.write("Synthesizing the retrieved information...")
                response = parse_response(result, query.strip())

                st.session_state.last_response = response.model_dump()
                st.session_state.last_query = query.strip()
                status.update(label="Research completed", state="complete", expanded=False)

            except Exception as exc:
                status.update(label="Research failed", state="error", expanded=True)
                st.error(f"Something went wrong: {exc}")
                st.info(
                    "If this is a deployment, verify that GROQ_API_KEY is present "
                    "in the Streamlit app's Secrets settings."
                )

if "last_response" in st.session_state:
    response = ResearchResponse.model_validate(st.session_state.last_response)

    st.divider()
    st.subheader(f"📌 {response.topic}")

    st.markdown("### Research Summary")
    st.write(response.summary)

    left, right = st.columns(2)

    with left:
        st.markdown("### 🧰 Tools Used")
        for tool_name in response.tools_used:
            st.write(f"- {tool_name}")

    with right:
        st.markdown("### 📚 Sources")
        if response.sources:
            for source in response.sources:
                st.write(f"- {source}")
        else:
            st.write("No explicit sources were returned.")

    st.divider()
    st.download_button(
        "⬇️ Download Research Report",
        data=make_report(response),
        file_name=f"agent_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

    with st.expander("View structured JSON"):
        st.json(response.model_dump())

else:
    st.info("Enter a question above and click **Research** to start.")
