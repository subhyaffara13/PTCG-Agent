
def _find_move_for_step(step: list[dict]) -> tuple[int, dict] | None:
    """Return ``(agent_idx, agent_record)`` for the agent that acted this step."""
    for j, agent in enumerate(step):
        action = agent.get("action")
        if not isinstance(action, dict):
            continue
        gr = action.get("generate_returns")
        astr = action.get("actionString")
        if gr and astr:
            return j, agent
    return None


def _find_move_for_step(step: list[dict]) -> tuple[int, dict] | None:
    """Return (agent_idx, agent_record) for the agent that played this step.

    The acting agent has a non-empty ``generate_returns`` and a populated
    ``actionString``. Returns ``None`` if no such agent (e.g. setup step).
    """
    for j, agent in enumerate(step):
        action = agent.get("action")
        if not isinstance(action, dict):
            continue
        gr = action.get("generate_returns")
        astr = action.get("actionString")
        if gr and astr:
            return j, agent
    return None


def _find_move_for_step(step: list[dict]) -> tuple[int, dict] | None:
    """Return (agent_idx, agent_record) for the agent that played this step.

    The acting agent has a non-empty ``generate_returns`` and a populated
    ``actionString``. Returns ``None`` if no such agent (e.g. setup step).
    """
    for j, agent in enumerate(step):
        action = agent.get("action")
        if not isinstance(action, dict):
            continue
        gr = action.get("generate_returns")
        astr = action.get("actionString")
        if gr and astr:
            return j, agent
    return None

