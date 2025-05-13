from langgraph.checkpoint.memory import InMemorySaver
from create_agents import (
    Receptionist,
    DietPreferenceParser,
    MedicalConditionAnalyzer
)
from langgraph_swarm import create_swarm
from dotenv import load_dotenv
import os


load_dotenv()


def load_langsmith():
    """
    Load the Langsmith environment for agent interaction.
    
    Returns:
        None
    """
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "diet-medical-receptionist-swarm"


def create_swarm_agents():
    """
    Create a swarm of agents for handling medical inquiries.
    
    Returns:
        Swarm: A compiled swarm of agents ready for interaction.
    """
    load_langsmith()

    memory = InMemorySaver()
    swarm = create_swarm(
        agents=[Receptionist, DietPreferenceParser, MedicalConditionAnalyzer],
        default_active_agent="Receptionist"
    ).compile(checkpointer=memory)
    return swarm