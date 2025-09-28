from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from langchain_groq import ChatGroq

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]  
    tools_used: list[str]


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query using the available tools if needed.
            
            Your FINAL answer MUST be a single valid JSON object that strictly follows this schema:
            {format_instructions}
            
            Do not include any explanations, markdown, code fences, or other text.
            Only output the JSON object.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response["output"])
    print("\n=== Structured Research Response ===")
    print("Topic:", structured_response.topic)
    print("Summary:", structured_response.summary)
    print("Sources:", ", ".join(structured_response.sources))
    print("Tools Used:", ", ".join(structured_response.tools_used))

    from tools import save_to_txt
    save_to_txt(structured_response.dict())  

except Exception as e:
    print("\nError parsing response:", e)
    print("Raw Response:", raw_response)
