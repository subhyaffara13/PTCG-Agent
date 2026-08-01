
def extract_tensors_from_args(
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> list[tuple[str, torch.Tensor]]:
    """Extract tensor arguments from captured aten args/kwargs.

    Unlike extract_tensors_from_sample which walks SampleInput pytrees,
    this walks the flat aten-level args and kwargs directly.
    """
    tensors: list[tuple[str, torch.Tensor]] = []
    idx = 0

    def _collect(x: Any) -> Any:
        nonlocal idx
        if isinstance(x, torch.Tensor):
            tensors.append((f"tensor_{idx}", x))
            idx += 1
        return x

    pytree.tree_map(_collect, args)
    pytree.tree_map(_collect, kwargs)
    return tensors

