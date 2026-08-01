
def _fused_dropout_decomposition(input, p, generator=None):
    if generator is not None:
        raise AssertionError(
            f"generator must be None for _fused_dropout decomposition, got {generator}"
        )
    mask = (torch.rand_like(input) < p).to(dtype=torch.uint8)
    res = mask.type_as(input) * input * (1.0 / p)
    return (res, mask)

