
def _is_named_optimizer(optim_state_dict: dict[str, Any]) -> bool:
    """
    Returns whether the state_dict is from a NamedOptimizer.
    This function checks that the keys in the state_dict['state'] are strings
    (which usually are FQNs) versus integers (which usually refer to param_ids
    from a vanilla torch.optim.Optimizer).
    """
    state = optim_state_dict.get("state")
    if not state:
        # If we cannot find a state, assume it is not NamedOptimizer as
        # NamedOptimizer has eager initialization.
        return False
    try:
        key = next(iter(state.keys()))
    except Exception as e:
        raise Exception(optim_state_dict) from e  # noqa: TRY002
    return isinstance(key, str)

