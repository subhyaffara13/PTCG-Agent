from typing import Any

def _get_param_to_param_id_from_optim_input(
    model: nn.Module,
    optim_input: list[dict[str, Any]] | Iterable[nn.Parameter] | None = None,
) -> dict[nn.Parameter, int]:
    """Constructs the inverse mapping of :func:`_get_param_id_to_param_from_optim_input`."""
    param_id_to_param = _get_param_id_to_param_from_optim_input(model, optim_input)
    return {param: param_id for param_id, param in param_id_to_param.items()}

