
def softmax(x: Tensor, dim: int, half_to_float: bool) -> Tensor:
    if half_to_float:
        if x.dtype not in [torch.half, torch.bfloat16]:
            raise AssertionError(
                f"half_to_float is True but x.dtype is {x.dtype}, expected half or bfloat16"
            )

    computation_dtype, result_dtype = utils.elementwise_dtypes(
        x, type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

    result_dtype = result_dtype if not half_to_float else computation_dtype
    res = torch.empty_like(x, dtype=result_dtype, memory_format=torch.contiguous_format)
    return res


def softmax(_outputs):
    maxes = np.max(_outputs, axis=-1, keepdims=True)
    shifted_exp = np.exp(_outputs - maxes)
    return shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)


def softmax(_outputs):
    maxes = np.max(_outputs, axis=-1, keepdims=True)
    shifted_exp = np.exp(_outputs - maxes)
    return shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)


def softmax(hidden_state, dim, onnx_trace=False):
    if onnx_trace:
        return nn.functional.softmax(hidden_state.float(), dim=dim)
    else:
        return nn.functional.softmax(hidden_state, dim=dim, dtype=torch.float32)


def softmax(
    input: Tensor | MaskedTensor,
    dim: int,
    *,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    mask_input = _combine_input_and_mask(amax, input, mask)
    if mask_input.layout == torch.strided:
        return torch.nn.functional.softmax(mask_input, dim_, dtype=dtype)
    else:
        raise ValueError(
            f"masked softmax expects strided tensor (got {mask_input.layout} tensor)"
        )


def softmax(
    input: Tensor,
    dim: int | None = None,
    _stacklevel: int = 3,
    dtype: DType | None = None,
) -> Tensor:
    r"""Apply a softmax function.

    Softmax is defined as:

    :math:`\text{Softmax}(x_{i}) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}`

    It is applied to all slices along dim, and will re-scale them so that the elements
    lie in the range `[0, 1]` and sum to 1.

    See :class:`~torch.nn.Softmax` for more details.

    Args:
        input (Tensor): input
        dim (int): A dimension along which softmax will be computed.
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
          If specified, the input tensor is casted to :attr:`dtype` before the operation
          is performed. This is useful for preventing data type overflows. Default: None.

    .. note::
        This function doesn't work directly with NLLLoss,
        which expects the Log to be computed between the Softmax and itself.
        Use log_softmax instead (it's faster and has better numerical properties).

    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            softmax, (input,), input, dim=dim, _stacklevel=_stacklevel, dtype=dtype
        )
    if dim is None:
        dim = _get_softmax_dim("softmax", input.dim(), _stacklevel)
    if dtype is None:
        ret = input.softmax(dim)
    else:
        ret = input.softmax(dim, dtype=dtype)
    return ret


def softmax(
    a: TensorLikeType,
    dim: int,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    result_dtype = dtype or a.dtype
    computation_dtype = utils.get_computation_dtype(result_dtype)
    a_ = _maybe_convert_to_dtype(a, computation_dtype)
    if a.numel() == 0:
        a_exp = exp(a_)
    else:
        a_max = amax(a_, dim, keepdim=True)
        a_exp = exp(a_ - a_max)
    return _maybe_convert_to_dtype(
        # pyrefly: ignore [no-matching-overload]
        true_divide(a_exp, sum(a_exp, dim, keepdim=True)),
        result_dtype,
    )  # type: ignore[return-value]


def softmax(
    a: TensorLikeType,
    dim: int,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    return torch.softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]


def softmax(
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
    return torch.softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]


def softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    softmax = g.op("Softmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        softmax = g.op(
            "Cast", softmax, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )

    return softmax


def softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    # Softmax does normalization at vector level.
    # PyTorch and ONNX use different strategies to split the input tensor into vectors.
    # Thus dim and axis have different meanings.
    # PyTorch slices the input tensor into vectors along the `dim`-th dimension.
    # ONNX reshapes the input into a 2-D tensor, and `axis` indicates where the input is coerced.
    # If input is a 2 x 3 tensor:
    # input = [[1.0, 1.0, 1.0],
    #          [1.0, 1,0, 1,0]]
    # with dim = 0, the result is:
    # result = [[0.5, 0.5, 0.5],
    #           [0.5, 0.5, 0.5]]
    # with axis = 0, the result is:
    # result = [[0.167, 0.167, 0.167],
    #           [0.167, 0.167, 0.167]]
    # So only when dim and axis both equal to ndim - 1 (the last dimension),
    # their semantics are equivalent.
    # So use softmax when dim and axis both equal to ndim - 1,
    # otherwise transpose the input to put the vectors to be normalized to the last dimension.
    # When input rank is not known at export time we compute softmax using a subgraph
    # with other operators
    input_dim = symbolic_helper._get_tensor_rank(input)
    if input_dim is not None:
        # TODO: remove this as onnx opset 11 spec allows negative axes
        if dim < 0:
            dim = input_dim + dim

        is_transpose_required = input_dim != dim + 1

        if is_transpose_required:
            axes = list(range(input_dim))
            axes[dim], axes[-1] = axes[-1], axes[dim]
            input = g.op("Transpose", input, perm_i=axes)
            dim = input_dim - 1

        softmax = g.op("Softmax", input, axis_i=dim)
        if dtype and dtype.node().kind() != "prim::Constant":
            parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
            softmax = g.op(
                "Cast",
                softmax,
                to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type(),
            )

        if is_transpose_required:
            softmax = g.op("Transpose", softmax, perm_i=axes)  # type: ignore[possibly-undefined]
        return softmax

    # Apply max normalization.
    input = g.op("Sub", input, g.op("ReduceMax", input, axes_i=[dim], keepdims_i=1))

    exp = g.op("Exp", input)
    sum = symbolic_helper._reducesum_helper(g, exp, axes_i=[dim])
    softmax = g.op("Div", exp, sum)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        softmax = g.op(
            "Cast", softmax, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    return softmax


def softmax(x, axis=None):
    r"""Compute the softmax function.

    The softmax function transforms each element of a collection by
    computing the exponential of each element divided by the sum of the
    exponentials of all the elements. That is, if `x` is a one-dimensional
    numpy array::

        softmax(x) = np.exp(x)/sum(np.exp(x))

    Parameters
    ----------
    x : array_like
        Input array.
    axis : int or tuple of ints, optional
        Axis to compute values along. Default is None and softmax will be
        computed over the entire array `x`.

    Returns
    -------
    s : ndarray
        An array the same shape as `x`. The result will sum to 1 along the
        specified axis.

    Notes
    -----
    The formula for the softmax function :math:`\sigma(x)` for a vector
    :math:`x = \{x_0, x_1, ..., x_{n-1}\}` is

    .. math:: \sigma(x)_j = \frac{e^{x_j}}{\sum_k e^{x_k}}

    The `softmax` function is the gradient of `logsumexp`.

    The implementation uses shifting to avoid overflow. See [1]_ for more
    details.

    .. versionadded:: 1.2.0

    References
    ----------
    .. [1] P. Blanchard, D.J. Higham, N.J. Higham, "Accurately computing the
       log-sum-exp and softmax functions", IMA Journal of Numerical Analysis,
       Vol.41(4), :doi:`10.1093/imanum/draa038`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import softmax
    >>> np.set_printoptions(precision=5)

    >>> x = np.array([[1, 0.5, 0.2, 3],
    ...               [1,  -1,   7, 3],
    ...               [2,  12,  13, 3]])
    ...

    Compute the softmax transformation over the entire array.

    >>> m = softmax(x)
    >>> m
    array([[  4.48309e-06,   2.71913e-06,   2.01438e-06,   3.31258e-05],
           [  4.48309e-06,   6.06720e-07,   1.80861e-03,   3.31258e-05],
           [  1.21863e-05,   2.68421e-01,   7.29644e-01,   3.31258e-05]])

    >>> m.sum()
    1.0

    Compute the softmax transformation along the first axis (i.e., the
    columns).

    >>> m = softmax(x, axis=0)

    >>> m
    array([[  2.11942e-01,   1.01300e-05,   2.75394e-06,   3.33333e-01],
           [  2.11942e-01,   2.26030e-06,   2.47262e-03,   3.33333e-01],
           [  5.76117e-01,   9.99988e-01,   9.97525e-01,   3.33333e-01]])

    >>> m.sum(axis=0)
    array([ 1.,  1.,  1.,  1.])

    Compute the softmax transformation along the second axis (i.e., the rows).

    >>> m = softmax(x, axis=1)
    >>> m
    array([[  1.05877e-01,   6.42177e-02,   4.75736e-02,   7.82332e-01],
           [  2.42746e-03,   3.28521e-04,   9.79307e-01,   1.79366e-02],
           [  1.22094e-05,   2.68929e-01,   7.31025e-01,   3.31885e-05]])

    >>> m.sum(axis=1)
    array([ 1.,  1.,  1.])

    """
    xp = array_namespace(x)
    x = xp.asarray(x)
    x_max = xp.max(x, axis=axis, keepdims=True)
    exp_x_shifted = xp.exp(x - x_max)
    return exp_x_shifted / xp.sum(exp_x_shifted, axis=axis, keepdims=True)


def softmax(x):
  unnormalized = np.exp(x - np.max(x))
  return unnormalized / np.sum(unnormalized)


def softmax(x):
  e = np.exp(x - np.max(x))
  return e / np.sum(e, axis=-1, keepdims=True)


def softmax(x):
  e = np.exp(x - np.max(x))
  return e / np.sum(e, axis=-1, keepdims=True)


def softmax(x):
  return np.exp(x) / np.sum(np.exp(x))


def softmax(x: ArrayLike,
            axis: Axis = -1,
            where: ArrayLike | None = None) -> Array:
  r"""Softmax function.

  Computes the function which rescales elements to the range :math:`[0, 1]`
  such that the elements along :code:`axis` sum to :math:`1`.

  .. math ::
    \mathrm{softmax}(x) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}

  Args:
    x : input array
    axis: the axis or axes along which the softmax should be computed. The
      softmax output summed across these dimensions should sum to :math:`1`.
      Either an integer, tuple of integers, or ``None`` (all axes).
    where: Elements to include in the :code:`softmax`. The output for any
      masked-out element is zero.

  Returns:
    An array.

  Note:
    If any input values are ``+inf``, the result will be all ``NaN``: this reflects the
    fact that ``inf / inf`` is not well-defined in the context of floating-point math.

  See also:
    :func:`log_softmax`
  """
  if config.softmax_custom_jvp.value:
    return _softmax(x, axis, where)
  else:
    return _softmax_deprecated(x, axis, where)


def softmax(x: ArrayLike,
            /,
            *,
            axis: int | tuple[int, ...] | None = None,
            ) -> Array:
  r"""Softmax function.

  JAX implementation of :func:`scipy.special.softmax`.

  Computes the function which rescales elements to the range :math:`[0, 1]`
  such that the elements along :code:`axis` sum to :math:`1`.

  .. math ::
    \mathrm{softmax}(x) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}

  Args:
    x : input array
    axis: the axis or axes along which the softmax should be computed. The
      softmax output summed across these dimensions should sum to :math:`1`.
      ``None`` means all axes.

  Returns:
    An array of the same shape as ``x``.

  Note:
    If any input values are ``+inf``, the result will be all ``NaN``: this
    reflects the fact that ``inf / inf`` is not well-defined in the context of
    floating-point math.

  See also:
    :func:`log_softmax`
  """
  return nn_softmax(x, axis=axis)


def softmax(
    x: jax.Array, *, axis: int = -1, num_warps: int = 4,
    interpret: bool = False, debug: bool = False
) -> jax.Array:
  """Computes the softmax of the input array along the specified axis.

  Args:
    x: input array
    axis: the axis along which to perform the computation
    num_warps: the number of warps to use for executing the Triton kernel
    interpret: whether to interpret the kernel using pallas
    debug: whether to use pallas in debug mode

  Returns:
    The result of the softmax operation over the specified axis of x.
  """
  axis = axis if axis >= 0 else len(x.shape) + axis
  if axis != len(x.shape) - 1:
    raise NotImplementedError(
        "reductions along non-trailing dimension unsupported")

  row_len = x.shape[-1]

  block_row = pl.next_power_of_2(row_len)
  out_shape = jax.ShapeDtypeStruct(shape=(row_len,), dtype=x.dtype)

  kernel = functools.partial(_vmappable_softmax_kernel, block_row=block_row)
  f = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(
          num_warps=num_warps, num_stages=1),
      grid=(),
      out_shape=out_shape,
      debug=debug,
      interpret=interpret,
  )

  for _ in range(len(x.shape) - 1):
    f = jax.vmap(f)

  return f(x)

