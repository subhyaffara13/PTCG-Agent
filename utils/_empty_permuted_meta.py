
def _empty_permuted_meta(
    shape: ShapeType,
    physical_layout: DimsSequenceType,
    *,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
) -> TensorLikeType:
    p_strides = utils.make_contiguous_strides_for([shape[l] for l in physical_layout])
    dim = len(shape)
    torch._check(
        len(physical_layout) == dim,
        lambda: (
            "Number of dimensions in the tensor input does not match the "
            f"length of the physical layout; i.e. len(size) = {dim} "
            f"is not equal to len(physical_layout) = {len(physical_layout)}"
        ),
    )
    strides = [0] * len(shape)
    seen_dims = set()
    for p, l in enumerate(physical_layout):
        torch._check(
            0 <= l < dim,
            lambda: (
                f"Dimension out of range (expected to be between 0 and {dim - 1}, but got "
                f"{l} at index {p}).  NB: negative dims "
                "not currently supported; file an issue if you want it."
            ),
        )
        torch._check(l not in seen_dims, lambda: "Duplicate dim not allowed")
        strides[l] = p_strides[p]
        seen_dims.add(l)
    return TensorMeta(
        shape=shape,
        strides=strides,
        dtype=dtype,
        device=device,
    )

