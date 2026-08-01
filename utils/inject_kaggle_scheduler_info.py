
def inject_kaggle_scheduler_info(agents_from_config, env):
    """
    TODO: this is a temporary hack to inject additional info from kaggle scheduler to set up agents. To be removed once
        scheduler has run config generator plugin.
    """
    kaggle_agents_info = env.info.get("Agents")
    if kaggle_agents_info and isinstance(kaggle_agents_info, list):
        for agent, kaggle_agent_info in zip(agents_from_config, kaggle_agents_info):
            display_name = kaggle_agent_info.get("Name", "")
            agent["display_name"] = display_name or agent.get("display_name", "")
            agent["thumbnail"] = kaggle_agent_info.get("ThumbnailUrl", "")

