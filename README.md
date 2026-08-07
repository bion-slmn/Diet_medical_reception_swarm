# Diet & Medical Receptionist Swarm

A multi-agent conversational system built with **LangGraph Swarm** that routes user inquiries between a receptionist, a diet-preference parser, and a medical-condition analyzer — each agent handing off control to the others as the conversation requires.

## Overview

This project implements an agentic "swarm" architecture where three specialized [`langgraph.prebuilt.create_react_agent`](https://langchain-ai.github.io/langgraph/) agents collaborate on a single conversation thread:

- **Receptionist** — the default entry point for all conversations. Greets the user, understands the initial request, and routes to the appropriate specialist.
- **DietPreferenceParser** — extracts and structures the user's dietary preferences, restrictions, and goals.
- **MedicalConditionAnalyzer** — extracts and analyzes any medical conditions or health context relevant to the user's request.

Agents can transfer control to one another via handoff tools, and all three share a `smart_search` tool for looking up external information. Conversation state and agent handoffs are persisted using an in-memory checkpointer, so the swarm remembers where it left off across turns.

## Architecture

```
                ┌─────────────────┐
     ┌─────────▶│   Receptionist   │◀─────────┐
     │          │  (default agent) │          │
     │          └────────┬─────────┘          │
     │                   │                     │
     │   transfer_to_*   │   transfer_to_*     │
     │                   ▼                     │
┌────┴──────────────┐        ┌─────────────────┴────┐
│ DietPreference     │◀──────▶│ MedicalCondition      │
│ Parser             │        │ Analyzer              │
└────────────────────┘        └───────────────────────┘

   All agents also have access to: smart_search
```

Each agent is a ReAct-style agent (reason + act) equipped with:
1. **Handoff tools** (`transfer_to_*`) to pass the conversation to a different agent.
2. **`smart_search`** for retrieving external/contextual information.

The swarm is compiled with `langgraph_swarm.create_swarm`, which wires the agents together and manages routing based on each agent's tool calls, starting from the `Receptionist` by default.

## Project Structure

```
.
├── create_agents.py     # Defines and instantiates the three ReAct agents
├── swarm.py              # Builds and compiles the LangGraph swarm (entry point)
├── load_llm.py           # LLM loader/factory used by all agents
├── prompt.py              # System prompts: Recaptionistprompt, Diet_prompt, Medical_prompt
├── tools.py               # Tool definitions: transfer_to_*, smart_search
├── .env                   # Environment variables (not committed)
└── README.md
```

## Prerequisites

- Python 3.10+
- A LangChain-compatible LLM provider configured in `load_llm.py`
- (Optional) A [LangSmith](https://smith.langchain.com/) account for tracing

## Installation

```bash
git clone <your-repo-url>
cd <repo-directory>
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Typical dependencies include:

```
langgraph
langgraph-swarm
langchain
python-dotenv
```

## Environment Variables

Create a `.env` file in the project root:

```env
LANGSMITH_API_KEY=your_langsmith_api_key
# Add any LLM provider credentials required by load_llm.py
# e.g. OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY, etc.
```

LangSmith tracing is enabled automatically when the swarm is created (`LANGSMITH_TRACING=true`, project name `diet-medical-receptionist-swarm`). If you don't want tracing, remove or comment out the `load_langsmith()` call in `swarm.py`.

## Usage

Build and invoke the swarm from Python:

```python
from swarm import create_swarm_agents

app = create_swarm_agents()

config = {"configurable": {"thread_id": "user-123"}}

response = app.invoke(
    {"messages": [{"role": "user", "content": "I'm diabetic and want a low-carb meal plan"}]},
    config=config,
)

print(response["messages"][-1].content)
```

Because the swarm is compiled with an `InMemorySaver` checkpointer, subsequent calls using the same `thread_id` will continue the conversation with full context, including which agent is currently active.

### How Handoffs Work

- The **Receptionist** starts every new conversation.
- If the user mentions dietary needs, it calls `transfer_to_DietPreferenceParser`.
- If the user mentions medical/health conditions, it calls `transfer_to_MedicalConditionAnalyzer`.
- Each specialist agent can hand back to the `Receptionist` or to the other specialist as needed (e.g., a medical condition that affects diet).
- `smart_search` is available to every agent for pulling in outside information (e.g., nutrition facts, medical guidance) during reasoning.

## Customization

- **Prompts**: Edit `Recaptionistprompt`, `Diet_prompt`, and `Medical_prompt` in `prompt.py` to change each agent's persona, instructions, and routing logic.
- **Tools**: Add new tools in `tools.py` and attach them to the relevant agent in `create_agents.py`.
- **LLM**: Swap models/providers by editing `load_llm.py` — all three agents share the same loader.
- **Persistence**: Replace `InMemorySaver` in `swarm.py` with a persistent checkpointer (e.g., SQLite, Postgres) for production use, since in-memory state is lost on process restart.

## Notes & Limitations

- `InMemorySaver` does not persist across process restarts — swap in a durable checkpointer before deploying.
- This system is not a substitute for professional medical or dietary advice; the `MedicalConditionAnalyzer` and `DietPreferenceParser` agents are intended to gather and structure user-provided information, not to diagnose or prescribe.
- Ensure any LLM provider API keys and LangSmith keys are kept out of version control (`.env` should be gitignored).

## License

Add your license of choice here (e.g., MIT).
