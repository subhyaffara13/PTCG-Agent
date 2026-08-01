
def promote_tensors(
    *tensors: ComplexTensor,
) -> tuple[torch.dtype, tuple[ComplexTensor, ...]]: ...


def promote_tensors(
    *tensors: Tensor,
) -> tuple[torch.dtype, tuple[Tensor, ...]]: ...


def promote_tensors(
    *tensors: Tensor | ComplexTensor,
) -> tuple[torch.dtype, tuple[Tensor | ComplexTensor, ...]]:
    """
    Promotes all tensors to a common dtype.
    Additionally promotes CPU tensors to at least `float32`.
    """
    tensor = next(t for t in tensors if isinstance(t, Tensor))
    out_dt = tensor.dtype
    for t in tensors:
        if isinstance(t, Tensor):
            out_dt = torch.promote_types(out_dt, t.dtype)

    prom_dt = PROMOTE_TYPES.get(out_dt, out_dt)
    return out_dt, tuple(
        t.to(prom_dt) if isinstance(t, Tensor) else torch.asarray(t, dtype=prom_dt)
        for t in tensors
    )

