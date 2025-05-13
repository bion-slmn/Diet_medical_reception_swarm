
from create_swarm import create_swarm_agents


swarm = create_swarm_agents()

config = {"configurable": {"thread_id": 12}}

for chunk in swarm.stream(
    {"messages": [{"role": "user", "content": "malaria in kenya how can i prevent and the cure?"}]},
    config,
    stream_mode="values", 
):
    print(chunk['messages'][-1].pretty_print()) # Access the last message directly