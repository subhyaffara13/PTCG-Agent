from typing import Callable, Dict

def register_agents(agent_dict: Dict[str, Callable]):
    agents.update(agent_dict)

