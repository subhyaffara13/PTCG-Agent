
def _get_param_to_param_key(
    optim: torch.optim.Optimizer,
    model: nn.Module | None = None,
    is_named_optimizer: bool = False,
    param_to_fqns: dict[nn.Parameter, list[str]] | None = None,
    flat_param_to_fqn: dict[FlatParameter, str] | None = None,
) -> dict[nn.Parameter, int | str]:
    """
    Constructs the inverse mapping of :func:`_get_param_key_to_param`. This API
    only supports the case where `optim` is a regular optimizer, not NamedOptimizer.
    So the parameter keys will be parameter ids.
    """
    param_id_to_param = _get_param_key_to_param(
        optim, model, is_named_optimizer, param_to_fqns, flat_param_to_fqn
    )
    return {param: param_id for param_id, param in param_id_to_param.items()}

