
def amax(
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

    mask_input = _combine_input_and_mask(amax, input, mask)
    dim_ = _canonical_dim(dim, mask_input.ndim)
    if mask_input.layout == torch.strided:
        return torch.amax(mask_input, dim_, bool(keepdim)).to(dtype=dtype)
    elif mask_input.layout == torch.sparse_coo:
        if mask is None:
            # See comment in the sparse_csr branch of prod, a similar issue arises here
            # where unspecified elements along a dimension may need to be reduced with the result
            raise ValueError(
                "masked amax expects explicit mask for sparse_coo tensor input"
            )
        return _sparse_coo_scatter_reduction_helper(
            torch.amax, mask_input, dim_, bool(keepdim), dtype
        )
    elif mask_input.layout == torch.sparse_csr:
        if mask is None:
            raise ValueError(
                "masked amax expects explicit mask for sparse_csr tensor input"
            )
        return _sparse_csr_segment_reduction_helper(
            torch.amax, mask_input, dim_, bool(keepdim), dtype
        )
    else:
        raise ValueError(
            f"masked amax expects strided, sparse_coo or sparse_csr tensor (got {mask_input.layout} tensor)"
        )


def amax(
    self: torch.Tensor,
    dim: int | None = None,
    keepdim: bool = False,
) -> torch.Tensor:
    if self.dtype == torch.bool:
        return torch.any(self, dim=dim, keepdim=keepdim)
    return NotImplemented


def amax(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
    initial: NotImplementedType = None,
    where: NotImplementedType = None,
):
    if a.is_complex():
        raise NotImplementedError(f"amax with dtype={a.dtype}")

    return a.amax(axis)


def amax(
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
        prims.amax,
        dims=dim,
        keepdims=keepdim,
        dtype=None,
        out=out,
        has_identity=False,
        output_dtype_kind=REDUCTION_OUTPUT_TYPE_KIND.SAME,
    )


def amax(g: jit_utils.GraphContext, self, dim, keepdim):
    axes = g.op("Constant", value_t=torch.tensor(dim, dtype=torch.long))
    return g.op("ReduceMax", self, axes, keepdims_i=keepdim)


def amax(g: jit_utils.GraphContext, self, dim, keepdim):
    return g.op("ReduceMax", self, axes_i=dim, keepdims_i=keepdim)


def amax(a, axis=None, out=None, keepdims=np._NoValue, initial=np._NoValue,
         where=np._NoValue):
    """
    Return the maximum of an array or maximum along an axis.

    `amax` is an alias of `~numpy.max`.

    See Also
    --------
    max : alias of this function
    ndarray.max : equivalent method
    """
    return _wrapreduction(a, np.maximum, 'max', axis, None, out,
                          keepdims=keepdims, initial=initial, where=where)


def amax(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  """Alias of :func:`jax.numpy.max`."""
  return max(a, axis=axis, out=out, keepdims=keepdims,
             initial=initial, where=where)

