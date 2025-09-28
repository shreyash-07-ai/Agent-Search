
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import json

def save_to_txt(data: str, filename: str = None):
    try:
        if isinstance(data, str):
            data = json.loads(data)
    except Exception:
        data = {"raw": data}
    
    if not filename:
        filename = f"research_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"Topic: {data.get('topic','')}\n\n"
        f"Summary:\n{data.get('summary', data.get('raw',''))}\n\n"
        f"Sources: {', '.join(data.get('sources', []))}\n"
        f"Tools Used: {', '.join(data.get('tools_used', []))}\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"✅ Data successfully saved to {filename}"


save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file."
)

search_tool = Tool(
    name="search",
    func=DuckDuckGoSearchRun().run,
    description="Search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=10000)
wiki_tool = Tool(
    name="wikipedia",                                   # <<< important
    func=WikipediaQueryRun(api_wrapper=api_wrapper).run,
    description="Fetch information from Wikipedia"
)
