
def is_collective_or_wait(n: fx.Node) -> bool:
    """Check if node is a collective start or wait."""
    if _schedulable_wait_node(n):
        return True
    # Collective starts have exactly one use: the wait_tensor
    if len(n.users) == 1:
        user = next(iter(n.users.keys()))
        if _schedulable_wait_node(user):
            return True
    return False

