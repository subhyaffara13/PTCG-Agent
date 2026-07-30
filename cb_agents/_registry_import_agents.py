from typing import Dict

_AGENT_REGISTRY: Dict[str, dict] = {}

def get_registered_agents() -> Dict[str, dict]:
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
    _AGENT_REGISTRY.clear()
