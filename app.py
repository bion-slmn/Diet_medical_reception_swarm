import streamlit as st
from create_swarm import create_swarm_agents

# Initialize swarm agents
swarm = create_swarm_agents()

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🧠 Swarm AI Medical Assistant")

# User input
user_input = st.text_input("Ask a question", "what foods can I eat when infected with COVID?")

# Send button
if st.button("Send"):
    config = {"configurable": {"thread_id": 12}}
    all_chunks = []

    with st.spinner("Thinking..."):
        # Stream response from swarm
        for chunk in swarm.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values",
        ):
            message = chunk["messages"][-1]
            all_chunks.append(message)

    # Store new messages in session
    st.session_state.messages.extend(all_chunks)

# Display all messages
st.subheader("Conversation History")
for msg in st.session_state.messages:
    role = getattr(msg, "role", "system").capitalize()
    content = getattr(msg, "content", str(msg))  # Fallback to str(msg) if no content attr
    st.markdown(f"**{role}:** {content}")
