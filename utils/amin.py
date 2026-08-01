
def amin(
    input: Tensor | MaskedTensor,
    dim: DimOrDims = None,
    *,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

{reduction_identity_dtype}

{reduction_args}

{reduction_example}"""
    if dtype is None:
        dtype = input.dtype

    mask_input = _combine_input_and_mask(amin, input, mask)
    dim_ = _canonical_dim(dim, mask_input.ndim)
    if mask_input.layout == torch.strided:
        return torch.amin(mask_input, dim_, bool(keepdim)).to(dtype=dtype)
    elif mask_input.layout == torch.sparse_coo:
        if mask is None:
            # See comment in the sparse_csr branch of prod, a similar issue arises here
            # where unspecified elements along a dimension may need to be reduced with the result
            raise ValueError(
                "masked amax expects explicit mask for sparse_coo tensor input"
            )
        return _sparse_coo_scatter_reduction_helper(
            torch.amin, mask_input, dim_, bool(keepdim), dtype
        )
    elif mask_input.layout == torch.sparse_csr:
        if mask is None:
            raise ValueError(
                "masked amin expects explicit mask for sparse_csr tensor input"
            )
        return _sparse_csr_segment_reduction_helper(
            torch.amin, mask_input, dim_, bool(keepdim), dtype
        )
    else:
        raise ValueError(
            f"masked amin expects strided, sparse_coo or sparse_csr tensor (got {mask_input.layout} tensor)"
        )


def amin(
    self: torch.Tensor,
    dim: int | None = None,
    keepdim: bool = False,
) -> torch.Tensor:
    if self.dtype == torch.bool:
        return torch.all(self, dim=dim, keepdim=keepdim)
    return NotImplemented


def amin(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
    initial: NotImplementedType = None,
    where: NotImplementedType = None,
):
    if a.is_complex():
        raise NotImplementedError(f"amin with dtype={a.dtype}")

    return a.amin(axis)


def amin(
    a: TensorLikeType,
    dim: DimsType | None = None,
    keepdim: bool = False,
    *,
    out: Tensor | None = None,
) -> TensorLikeType:
    # reduces over all dimensions if dim=() is passed
    if dim == () or dim == []:
        dim = None

    return _reduction(
        a,
        prims.amin,
        dims=dim,
        keepdims=keepdim,
        dtype=None,
        out=out,
        has_identity=False,
        output_dtype_kind=REDUCTION_OUTPUT_TYPE_KIND.SAME,
    )


def amin(g: jit_utils.GraphContext, self, dim, keepdim):
    axes = g.op("Constant", value_t=torch.tensor(dim, dtype=torch.long))
    return g.op("ReduceMin", self, axes, keepdims_i=keepdim)


def amin(g: jit_utils.GraphContext, self, dim, keepdim):
    return g.op("ReduceMin", self, axes_i=dim, keepdims_i=keepdim)


def amin(a, axis=None, out=None, keepdims=np._NoValue, initial=np._NoValue,
         where=np._NoValue):
    """
    Return the minimum of an array or minimum along an axis.

    `amin` is an alias of `~numpy.min`.

    See Also
    --------
    min : alias of this function
    ndarray.min : equivalent method
    """
    return _wrapreduction(a, np.minimum, 'min', axis, None, out,
                          keepdims=keepdims, initial=initial, where=where)


def amin(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  """Alias of :func:`jax.numpy.min`."""
  return min(a, axis=axis, out=out, keepdims=keepdims,
             initial=initial, where=where)

