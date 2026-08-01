from typing import Dict

def get_registered_agents() -> Dict[str, dict]:
    """
    Returns a *copy* of the current agent registry.
    """
    from cb_agents.registry import _AGENT_REGISTRY
    try:
        import importlib
        pkg = "cb_agents"
        for m in ["hand_analyst", "turn_planner", "strategy_agent", "opponent_model", "time_manager"]:
            try:
                importlib.import_module(f"{pkg}.{m}")
            except ImportError:
                pass
    except Exception:
        pass
    return dict(_AGENT_REGISTRY)
