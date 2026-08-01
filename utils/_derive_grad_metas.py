
def _derive_grad_metas(
    tensor_metas: tuple[TensorMeta, ...],
) -> tuple[_TensorMeta | None, ...]:
    """Derive gradient metadata from tensor metadata.

    Returns metadata with the same shape/stride/dtype but ``requires_grad=False``.
    Entries where the source has ``requires_grad=False`` become ``None``.
    """
    return tuple(
        _TensorMeta(shape=m.shape, stride=m.stride, dtype=m.dtype, requires_grad=False)
        if m.requires_grad
        else None
        for m in tensor_metas
    )

