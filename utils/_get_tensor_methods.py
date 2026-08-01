
def _get_tensor_methods() -> set[Callable]:
    """Returns a set of the overridable methods on ``torch.Tensor``"""
    overridable_funcs = get_overridable_functions()
    methods = set(overridable_funcs[torch.Tensor])
    return methods

