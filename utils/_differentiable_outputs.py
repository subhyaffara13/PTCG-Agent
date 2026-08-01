
def _differentiable_outputs(x):
    return tuple(o for o in _as_tuple(x) if o.requires_grad)

