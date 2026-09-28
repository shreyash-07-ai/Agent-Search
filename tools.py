from ddgs import DDGS
import wikipedia
from langchain.tools import Tool


def run_web_search(query: str) -> str:
    """Search the public web and return useful result titles, snippets and URLs."""
    try:
        results = list(DDGS().text(query, max_results=5))
        if not results:
            return "No web results were found."

        lines = []
        for index, item in enumerate(results, start=1):
            title = item.get("title", "Untitled")
            url = item.get("href", "")
            body = item.get("body", "")
            lines.append(f"{index}. {title}\nURL: {url}\nSnippet: {body}")

        return "\n\n".join(lines)
    except Exception as exc:
        return f"Web search failed: {exc}"


def run_wikipedia_search(query: str) -> str:
    """Retrieve a concise Wikipedia summary and page URL."""
    try:
        page = wikipedia.page(query, auto_suggest=True, redirect=True)
        summary = wikipedia.summary(query, sentences=6, auto_suggest=True, redirect=True)
        return (
            f"Title: {page.title}\n"
            f"URL: {page.url}\n"
            f"Summary: {summary}"
        )
    except Exception as exc:
        return f"Wikipedia lookup failed: {exc}"


search_tool = Tool(
    name="search",
    func=run_web_search,
    description=(
        "Search the public web for current or factual information. "
        "Use this when the question needs recent or broad web information. "
        "The results include URLs that can be used as source references."
    ),
)

wiki_tool = Tool(
    name="wikipedia",
    func=run_wikipedia_search,
    description=(
        "Search Wikipedia for background information about a topic, person, "
        "organization, technology, or historical subject. The result includes "
        "the Wikipedia page URL."
    ),
)
