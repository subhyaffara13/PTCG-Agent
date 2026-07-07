"""
agents/registry.py

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


def register_agent(
    bus_name: str,
    *,
    perspective_flag: str = "player",
    needs_skills_dir: bool = True,
    needs_shared_context: bool = True,
):
    """
    Class decorator that registers a sub-agent for automatic discovery.

    Parameters
    ----------
    bus_name : str
        The name used when calling ``RouterBus.register_agent(bus_name, ...)``.
    perspective_flag : str
        The perspective flag passed to ``RouterBus.register_agent`` (default ``"player"``).
    needs_skills_dir : bool
        If True the orchestrator will pass ``skills_dir`` to the constructor.
    needs_shared_context : bool
        If True the orchestrator will pass ``shared_context`` to the constructor.
    """

    def decorator(cls: Type) -> Type:
        if bus_name in _AGENT_REGISTRY:
            registered_cls = _AGENT_REGISTRY[bus_name]['cls'].__name__
            raise ValueError(
                f"Duplicate agent registration: bus_name '{bus_name}' "
                f"is already registered to {registered_cls}"
            )
        _AGENT_REGISTRY[bus_name] = {
            "cls": cls,
            "perspective_flag": perspective_flag,
            "needs_skills_dir": needs_skills_dir,
            "needs_shared_context": needs_shared_context,
        }
        return cls

    return decorator


def get_registered_agents() -> Dict[str, dict]:
    """
    Returns a *copy* of the current agent registry.

    Each value is a dict with keys:
        cls                 – the agent class
        perspective_flag    – 'player' or 'opponent'
        needs_skills_dir    – bool
        needs_shared_context – bool
    """
    try:
        import importlib
        pkg = __package__ or "agents"
        for m in ["hand_analyst", "turn_planner", "strategy_agent", "opponent_model", "time_manager"]:
            try:
                importlib.import_module(f"{pkg}.{m}")
            except ImportError:
                pass
    except Exception:
        pass
    return dict(_AGENT_REGISTRY)


def clear_registry() -> None:
    """Clears the registry.  Useful in tests to avoid cross-contamination."""
    _AGENT_REGISTRY.clear()
