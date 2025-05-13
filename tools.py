from langchain_community.tools import DuckDuckGoSearchResults
from langgraph_swarm import  create_handoff_tool



search = DuckDuckGoSearchResults(output_format="list")


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
