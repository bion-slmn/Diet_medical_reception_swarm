# app.py

import streamlit as st
from create_swarm import create_swarm_agents

# Initialize swarm agents
swarm = create_swarm_agents()

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Ask a question", "what foods can I eat when infected with COVID?")

if st.button("Send"):
    # Configuration
    config = {"configurable": {"thread_id": 12}}

    # Placeholder to show streamed messages as they arrive
    placeholder = st.empty()

    # Track messages
    all_chunks = []

    # Stream messages from the swarm
    for chunk in swarm.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    ):
        message = chunk['messages'][-1]
        all_chunks.append(message)

        # Display latest message (converted to string or pretty_print)
        placeholder.markdown(f"**{getattr(message, 'content', '')}")

    # Store full conversation in session
    st.session_state.messages.extend(all_chunks)



