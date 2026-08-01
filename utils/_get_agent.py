
def _get_agent(agent_id: str):
    """Look up an agent by ID or name. Returns None if not found."""
    from litellm.proxy.agent_endpoints.agent_registry import global_agent_registry

    agent = global_agent_registry.get_agent_by_id(agent_id=agent_id)
    if agent is None:
        agent = global_agent_registry.get_agent_by_name(agent_name=agent_id)
    return agent

