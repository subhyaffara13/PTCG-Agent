
def load_agent_pool(config_paths: list[str]) -> list[dict]:
    """Loads agent configurations from multiple YAML files and combines them."""
    agent_pool = []
    for path in config_paths:
        with open(path, "r") as f:
            agents = yaml.safe_load(f)
            if isinstance(agents, list):
                agent_pool.extend(agents)
    return agent_pool

