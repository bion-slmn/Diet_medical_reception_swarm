from langchain_community.tools import DuckDuckGoSearchResults
from langgraph_swarm import  create_handoff_tool
from langchain_community.tools import TavilySearchResults, tool
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")

# Initialize the two search tools
tavily_search = TavilySearchResults(max_results=5)
duckduckgo_search = DuckDuckGoSearchResults(output_format="list")

@tool
def smart_search(query: str) -> list:
    """
    Searches the internet using Tavily. Falls back to DuckDuckGo if Tavily fails or returns no results.
    """
    try:
        results = tavily_search.run(query)
        if results and isinstance(results, list) and len(results) > 0:
            return results
        else:
            print("Tavily returned no results. Falling back to DuckDuckGo.")
    except Exception as e:
        print(f"Tavily search failed with error: {e}. Falling back to DuckDuckGo.")

    try:
        return duckduckgo_search.run(query)
    except Exception as e:
        print(f"DuckDuckGo search also failed: {e}")
        return ["Both search engines failed."]


transfer_to_MedicalConditionAnalyzer = create_handoff_tool(
    agent_name="MedicalConditionAnalyzer",
    description="Transfer user to the medical_condition assistant.",
)

transfer_to_DietPreferenceParser = create_handoff_tool(
    agent_name="DietPreferenceParser",
    description="Transfer user to the diet_preference assistant.",
)

transfer_to_receptionist = create_handoff_tool(
    agent_name="Receptionist",
    description="Transfer user to the receptionist assistant.",
)
