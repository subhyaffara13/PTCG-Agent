
def _get_unfold_shape_stride(
    a_shape: ShapeType, a_stride: StrideType, dimension: int, size: int, step: int
):
    a_ndim = len(a_shape)
    dim = utils.canonicalize_dim(a_ndim, dimension, wrap_scalar=True)
    max_size = 1 if a_ndim == 0 else a_shape[dim]
    last_stride = 1 if a_ndim == 0 else a_stride[dim]

    torch._check(
        size <= max_size,
        lambda: f"Maximum size for tensor at dimension {dim} is {max_size} but size is {size}",
    )

    torch._check(
        step > 0,
        lambda: f"Step is {step} but must be > 0",
    )

    shape = list(a_shape)
    strides = list(a_stride)
    shape.append(size)
    strides.append(last_stride)
    if dim < a_ndim:
        shape[dim] = (shape[dim] - size) // step + 1
        strides[dim] *= step
    return shape, strides

