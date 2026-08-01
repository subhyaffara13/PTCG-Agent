
def all_reduce_forward(x, device_mesh):
    """All-reduce forward, identity backward. Use after rowwise layers."""
    return _AllReduceForward.apply(x, device_mesh)

