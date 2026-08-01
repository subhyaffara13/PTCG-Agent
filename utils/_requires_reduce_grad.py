
def _requires_reduce_grad(action_type: _ComputationType) -> bool:
    return action_type in (W, B)

