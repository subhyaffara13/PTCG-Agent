
def _get_active_index(state):
    """Return the index of the ACTIVE agent, or None if none."""
    for i in range(2):
        if state[i].status == "ACTIVE":
            return i
    return None

