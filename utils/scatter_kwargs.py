
def scatter_kwargs(
    inputs: tuple[Any, ...],
    kwargs: dict[str, Any] | None,
    target_gpus: Sequence[int | torch.device],
    dim: int = 0,
) -> tuple[tuple[Any, ...], tuple[dict[str, Any], ...]]:
    r"""Scatter with support for kwargs dictionary."""
    scattered_inputs = scatter(inputs, target_gpus, dim) if inputs else []
    scattered_kwargs = scatter(kwargs, target_gpus, dim) if kwargs else []
    if len(scattered_inputs) < len(scattered_kwargs):
        scattered_inputs.extend(
            () for _ in range(len(scattered_kwargs) - len(scattered_inputs))
        )
    elif len(scattered_kwargs) < len(inputs):
        scattered_kwargs.extend(
            {} for _ in range(len(scattered_inputs) - len(scattered_kwargs))
        )
    return tuple(scattered_inputs), tuple(scattered_kwargs)

