from load_llm import load_llm
from langgraph.prebuilt import create_react_agent
from prompt import Diet_prompt, Recaptionistprompt, Medical_prompt
from tools import (
    transfer_to_MedicalConditionAnalyzer,
    transfer_to_DietPreferenceParser,
    transfer_to_receptionist,
    smart_search
)


llm = load_llm()

Receptionist = create_react_agent(
    llm,
    tools=[
        transfer_to_MedicalConditionAnalyzer,
        transfer_to_DietPreferenceParser,
        smart_search],
    prompt= Recaptionistprompt,
    name="Receptionist",
    
)

DietPreferenceParser = create_react_agent(
    llm,
    tools=[
        transfer_to_MedicalConditionAnalyzer,
        transfer_to_receptionist,
        smart_search],
    prompt= Diet_prompt,
    name="DietPreferenceParser",
    
)

MedicalConditionAnalyzer = create_react_agent(
    llm,
    tools=[
        transfer_to_DietPreferenceParser,
        transfer_to_receptionist,
        smart_search],
    prompt= Medical_prompt,
    name="MedicalConditionAnalyzer",
    
)