
def _noop_agent(observation, configuration):
    """Agent that always ends its turn immediately (does nothing)."""
    return [{"type": "end_turn"}]

