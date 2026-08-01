"""
cb_agents/registry.py

Decorator-based agent registration system.
Each sub-agent class decorates itself with @register_agent to declare its
bus name, constructor parameter requirements, and optional RouterBus metadata.
The Orchestrator discovers all registered agents via get_registered_agents()
instead of hardcoding imports.
"""

from typing import Any, Callable, Dict, List, Optional, Type

# ---------------------------------------------------------------------------
# Internal registry storage
# ---------------------------------------------------------------------------
_AGENT_REGISTRY: Dict[str, dict] = {}


from utils.register_agent import register_agent


from utils.get_registered_agents import get_registered_agents


from utils.clear_registry import clear_registry
