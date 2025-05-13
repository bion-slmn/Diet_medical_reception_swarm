import streamlit as st
import uuid
from create_swarm import create_swarm_agents

# Initialize swarm agents
swarm = create_swarm_agents()

# Generate a unique session-based thread ID if not already created
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 SmartCare: Your AI-Powered Medical & Diet Assistant")


# Expandable description
with st.expander("ℹ️ About this Assistant"):
    st.markdown("""
This assistant is powered by a Swarm of three specialized AI agents:

- **Receptionist**: Handles general questions and redirects you to the right specialist.
- **Diet Specialist**: Offers advice on food, nutrition, and dietary preferences — even in the context of medical conditions.
- **Medical Officer**: Helps analyze symptoms, conditions, or health concerns and suggests appropriate action or guidance.

The system intelligently routes your questions to the most relevant agent and can pass questions across agents when needed.
""")

# User input
user_input = st.text_input(
    "Ask a question",
    placeholder="e.g. What foods are good for someone with diabetes?"
)


# Send button
if st.button("Send") and user_input.strip():
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    all_chunks = []

    with st.spinner("Thinking..."):
        for chunk in swarm.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values",  # Could also try "messages" if supported
        ):
            msg = chunk["messages"][-1]  # Safely extract the last message

            # Determine the role
            if hasattr(msg, "role"):
                role = msg.role.capitalize()
            elif hasattr(msg, "name"):
                role = msg.name or 'User'
            else:
                role = "System"

            content = getattr(msg, "content", str(msg))

            all_chunks.append(msg)
            st.markdown(f"**{role}:** {content}")

    # Store messages in session state
    st.session_state.messages.extend(all_chunks)
