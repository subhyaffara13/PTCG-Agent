
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

