
def _iter_tensors(
    x: torch.Tensor | Iterable[torch.Tensor], only_requiring_grad: bool = False
) -> Iterable[torch.Tensor]:
    if is_tensor_like(x):
        # mypy doesn't narrow type of `x` to torch.Tensor
        if x.requires_grad or not only_requiring_grad:  # type: ignore[union-attr]
            yield x  # type: ignore[misc]
    elif isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
        for elem in x:
            yield from _iter_tensors(elem, only_requiring_grad)

