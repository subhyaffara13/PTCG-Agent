from typing import Dict

_AGENT_REGISTRY: Dict[str, dict] = {}

from utils.get_registered_agents import get_registered_agents

from utils.clear_registry import clear_registry
