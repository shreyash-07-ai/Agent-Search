from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool


def run_web_search(query: str) -> str:
    """Search the public web using DuckDuckGo."""
    try:
        return DuckDuckGoSearchRun().invoke(query)
    except Exception as exc:
        return f"Web search failed: {exc}"


def run_wikipedia_search(query: str) -> str:
    """Retrieve background information from Wikipedia."""
    try:
        return WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=8000,
            )
        ).invoke(query)
    except Exception as exc:
        return f"Wikipedia lookup failed: {exc}"


search_tool = Tool(
    name="search",
    func=run_web_search,
    description=(
        "Search the public web for current or factual information. "
        "Use this when the question needs recent or broad web information."
    ),
)

wiki_tool = Tool(
    name="wikipedia",
    func=run_wikipedia_search,
    description=(
        "Search Wikipedia for reliable background information about a topic, "
        "person, organization, technology, or historical subject."
    ),
)
