from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import json

def save_to_txt(data: str, filename: str = None):
    """Save structured research data (JSON or dict) into a well-formatted text file."""
    
    # Convert string JSON to dict (if needed)
    try:
        if isinstance(data, str):
            data = json.loads(data)
    except Exception:
        # If not JSON, just wrap it as raw text
        data = {"raw": data}
    
    # Generate unique filename if not provided
    if not filename:
        timestamp_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_output_{timestamp_name}.txt"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format nicely
    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"Topic: {data.get('topic', '')}\n\n"
        f"Summary:\n{data.get('summary', data.get('raw', ''))}\n\n"
        f"Sources: {', '.join(data.get('sources', [])) if 'sources' in data else ''}\n"
        f"Tools Used: {', '.join(data.get('tools_used', [])) if 'tools_used' in data else ''}\n"
    )

    with open(filename, "w", encoding="utf-8") as f:  # overwrite new file each time
        f.write(formatted_text)

    return f"✅ Data successfully saved to {filename}"

# Register tool
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data (topic, summary, sources, tools) to a text file."
)

# Other tools stay same
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=10000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
