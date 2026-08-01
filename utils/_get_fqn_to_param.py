
def _get_fqn_to_param(
    model: torch.nn.Module,
) -> dict[str, torch.nn.Parameter]:
    """Construct the inverse mapping of :meth:`_get_param_to_fqn`."""
    param_to_param_name = _get_param_to_fqn(model)
    return dict(zip(param_to_param_name.values(), param_to_param_name.keys()))

