
def _mark_agent_loss(state, losing_idx):
    """Mark the agent at losing_idx as having lost."""
    state[losing_idx].status = "DONE"
    state[losing_idx].reward = -1
    state[1 - losing_idx].reward = 1
    state[1 - losing_idx].status = "DONE"

