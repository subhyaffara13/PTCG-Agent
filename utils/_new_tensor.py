
def _new_tensor(
    t: Any,
    new_shape: Sequence[int] | None = None,
    new_stride: Sequence[int] | None = None,
) -> Any:
    if isinstance(t, torch.Tensor):
        if type(t) not in (FunctionalTensor, FakeTensor, torch.Tensor):
            raise AssertionError(f"No subclasses support for now, found {type(t)}")
        return torch.empty_strided(
            t.size() if new_shape is None else new_shape,
            t.stride() if new_stride is None else new_stride,
            device=t.device,
            dtype=t.dtype,
            requires_grad=t.requires_grad,
        )
    return t

