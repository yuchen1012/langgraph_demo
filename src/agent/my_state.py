from langgraph.prebuilt.chat_agent_executor import AgentState


class MyState(AgentState):
    username: str
