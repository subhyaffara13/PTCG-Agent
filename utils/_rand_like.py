
def _rand_like(
    rand_fn: Callable[..., torch.Tensor],
    self: torch.Tensor,
    *,
    dtype: torch.dtype | None = None,
    device: torch.device | None = None,
    memory_format: torch.memory_format = torch.preserve_format,
    **kwargs: Any,
) -> torch.Tensor:
    dtype = self.dtype if dtype is None else dtype
    device = self.device if device is None else device

    if memory_format != torch.preserve_format:
        return rand_fn(
            self.shape,
            dtype=dtype,
            device=device,
            **kwargs,
        ).to(memory_format=memory_format)

    shape, permutation = _get_shape_permutation_like(self)
    result = rand_fn(
        shape,
        dtype=dtype,
        device=device,
        **kwargs,
    )
    if permutation == list(range(len(permutation))):
        return result
    return result.permute(permutation).clone()

