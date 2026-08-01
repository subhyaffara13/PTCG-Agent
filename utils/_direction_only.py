
def _direction_only(action_string: str) -> str:
    """Strip the ``ant<i>:`` prefix from a legal action string.

    For ``ant0:up`` returns ``up``. If the action is already a bare
    direction, returns it unchanged.
    """
    if ":" in action_string:
        return action_string.split(":", 1)[1]
    return action_string

