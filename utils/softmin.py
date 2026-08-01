
def softmin(
    input: Tensor | MaskedTensor,
    dim: int,
    *,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    mask_input = _combine_input_and_mask(amin, input, mask)
    if mask_input.layout == torch.strided:
        return torch.nn.functional.softmin(mask_input, dim_, dtype=dtype)
    else:
        raise ValueError(
            f"masked softmin expects strided tensor (got {mask_input.layout} tensor)"
        )


def softmin(
    input: Tensor,
    dim: int | None = None,
    _stacklevel: int = 3,
    dtype: DType | None = None,
) -> Tensor:
    r"""Apply a softmin function.

    Note that :math:`\text{Softmin}(x) = \text{Softmax}(-x)`. See softmax definition for mathematical formula.

    See :class:`~torch.nn.Softmin` for more details.

    Args:
        input (Tensor): input
        dim (int): A dimension along which softmin will be computed (so every slice
            along dim will sum to 1).
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
          If specified, the input tensor is casted to :attr:`dtype` before the operation
          is performed. This is useful for preventing data type overflows. Default: None.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            softmin, (input,), input, dim=dim, _stacklevel=_stacklevel, dtype=dtype
        )
    if dim is None:
        dim = _get_softmax_dim("softmin", input.dim(), _stacklevel)
    if dtype is None:
        ret = (-input).softmax(dim)
    else:
        ret = (-input).softmax(dim, dtype=dtype)
    return ret


def softmin(
    a: TensorLikeType,
    dim: int | None = None,
    _stacklevel: int = 3,  # for compat when using TorchRefsMode(strict=True)
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    # The error is for compat with regular PyTorch, which has this behavior
    # deprecated.  For PrimTorch, it's fine to drop support for deprecated
    # behavior because it requires explicit opt in.  This error is to inform
    # users how to update their calls.
    torch._check(dim is not None, lambda: "implicit dim not supported, use dim=X")
    return torch.softmax(a=-a, dim=dim, dtype=dtype)  # type: ignore[call-overload]

