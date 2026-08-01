
def extract_tensor_metas(
    tensors: tuple[torch.Tensor, ...] | None,
    *,
    allow_none: Literal[False] = ...,
) -> tuple[TensorMeta, ...] | None: ...


def extract_tensor_metas(
    tensors: tuple[torch.Tensor | None, ...] | None,
    *,
    allow_none: Literal[True],
) -> tuple[TensorMeta | None, ...] | None: ...


def extract_tensor_metas(
    tensors: tuple[torch.Tensor | None, ...] | tuple[torch.Tensor, ...] | None,
    *,
    allow_none: bool = False,
) -> tuple[TensorMeta | None, ...] | None:
    """Extract metadata from a tuple of tensors.

    Args:
        tensors: Tuple of tensors (may include ``None`` when ``allow_none=True``).
        allow_none: If ``True``, preserve ``None`` elements (for gradients).

    Returns:
        Tuple of ``TensorMeta``, or ``None`` if ``tensors`` is ``None``.

    Raises:
        PipeliningMetadataError: If ``None`` found and ``allow_none=False``.
    """
    if tensors is None:
        return None

    metas_with_none: list[TensorMeta | None] = []
    has_none = False
    for t in tensors:
        if isinstance(t, torch.Tensor):
            metas_with_none.append(extract_tensor_meta(t))
        else:
            has_none = True
            metas_with_none.append(None)
    if not allow_none and has_none:
        raise PipeliningMetadataError(
            "None values are not allowed in tensor metadata tuples. "
            "Use allow_none=True for optional values."
        )
    return tuple(metas_with_none)

