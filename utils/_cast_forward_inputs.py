
def _cast_forward_inputs(
    dtype: torch.dtype | None,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, Any]:
    """
    Cast floating point tensors in ``args`` and ``kwargs`` to ``input_dtype``.

    This respects the existing ``requires_grad`` on the tensors.
    """
    if dtype is None:
        return args, kwargs

    def cast_fn(x: torch.Tensor) -> torch.Tensor:
        if not torch.is_floating_point(x) or x.dtype == dtype:
            return x

        return x.to(dtype)

    return (_apply_to_tensors(cast_fn, args), _apply_to_tensors(cast_fn, kwargs))

