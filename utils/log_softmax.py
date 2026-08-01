
def log_softmax(
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
        return torch.nn.functional.log_softmax(mask_input, dim_, dtype=dtype)
    else:
        raise ValueError(
            f"masked log_softmax expects strided tensor (got {mask_input.layout} tensor)"
        )


def log_softmax(
    input: Tensor,
    dim: int | None = None,
    _stacklevel: int = 3,
    dtype: DType | None = None,
) -> Tensor:
    r"""Apply a softmax followed by a logarithm.

    While mathematically equivalent to log(softmax(x)), doing these two
    operations separately is slower and numerically unstable. This function
    uses an alternative formulation to compute the output and gradient correctly.

    See :class:`~torch.nn.LogSoftmax` for more details.

    Args:
        input (Tensor): input
        dim (int): A dimension along which log_softmax will be computed.
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
          If specified, the input tensor is cast to :attr:`dtype` before the operation
          is performed. This is useful for preventing data type overflows. Default: None.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            log_softmax, (input,), input, dim=dim, _stacklevel=_stacklevel, dtype=dtype
        )
    if dim is None:
        dim = _get_softmax_dim("log_softmax", input.dim(), _stacklevel)
    if dtype is None:
        ret = input.log_softmax(dim)
    else:
        ret = input.log_softmax(dim, dtype=dtype)
    return ret


def log_softmax(
    a: TensorLikeType,
    dim: int,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    result_dtype = dtype or a.dtype
    computation_dtype = utils.get_computation_dtype(result_dtype)
    a_ = _maybe_convert_to_dtype(a, computation_dtype)
    return _maybe_convert_to_dtype(a_ - logsumexp(a_, dim, keepdim=True), result_dtype)  # type: ignore[return-value]


def log_softmax(
    a: TensorLikeType,
    dim: int,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    return torch.log_softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]


def log_softmax(
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
    return torch.log_softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]


def log_softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    return_op = g.op("LogSoftmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        return_op = g.op(
            "Cast", return_op, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    return return_op


def log_softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    # PyTorch dim and ONNX axis have different meanings.
    # See Softmax comment for details.
    # TODO: remove this as onnx opset 11 spec allows negative axes
    input_dim = symbolic_helper._get_tensor_rank(input)
    if input_dim is None:
        return symbolic_helper._unimplemented(
            "dim",
            "ONNX and PyTorch use different strategies to split the input. "
            "Input rank must be known at export time.",
        )
    if dim < 0:
        dim = input_dim + dim
    is_transpose_required = input_dim != dim + 1
    # ONNX only supports log_softmax with dim = -1. Transpose must be added before and after log_softmax to support other cases.
    if is_transpose_required:
        axes = list(range(input_dim))
        axes[dim], axes[-1] = axes[-1], axes[dim]
        input = g.op("Transpose", input, perm_i=axes)
        dim = input_dim - 1
    return_op = g.op("LogSoftmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        return_op = g.op(
            "Cast", return_op, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    if is_transpose_required:
        return_op = g.op("Transpose", return_op, perm_i=axes)  # type: ignore[possibly-undefined]
    return return_op


def log_softmax(x, axis=None):
    r"""Compute the logarithm of the softmax function.

    In principle::

        log_softmax(x) = log(softmax(x))

    but using a more accurate implementation.

    Parameters
    ----------
    x : array_like
        Input array.
    axis : int or tuple of ints, optional
        Axis to compute values along. Default is None and softmax will be
        computed over the entire array `x`.

    Returns
    -------
    s : ndarray or scalar
        An array with the same shape as `x`. Exponential of the result will
        sum to 1 along the specified axis. If `x` is a scalar, a scalar is
        returned.

    Notes
    -----
    `log_softmax` is more accurate than ``np.log(softmax(x))`` with inputs that
    make `softmax` saturate (see examples below).

    .. versionadded:: 1.5.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import log_softmax
    >>> from scipy.special import softmax
    >>> np.set_printoptions(precision=5)

    >>> x = np.array([1000.0, 1.0])

    >>> y = log_softmax(x)
    >>> y
    array([   0., -999.])

    >>> with np.errstate(divide='ignore'):
    ...   y = np.log(softmax(x))
    ...
    >>> y
    array([  0., -inf])

    """
    xp = array_namespace(x)
    x = xp.asarray(x)

    x_max = xp.max(x, axis=axis, keepdims=True)

    if x_max.ndim > 0:
        x_max = xpx.at(x_max, ~xp.isfinite(x_max)).set(0)
    elif not xp.isfinite(x_max):
        x_max = 0

    tmp = x - x_max
    exp_tmp = xp.exp(tmp)

    # suppress warnings about log of zero
    with np.errstate(divide='ignore'):
        s = xp.sum(exp_tmp, axis=axis, keepdims=True)
        out = xp.log(s)

    return tmp - out


def log_softmax(x: ArrayLike,
                axis: Axis = -1,
                where: ArrayLike | None = None) -> Array:
  r"""Log-Softmax function.

  Computes the logarithm of the :code:`softmax` function, which rescales
  elements to the range :math:`[-\infty, 0)`.

  .. math ::
    \mathrm{log\_softmax}(x)_i = \log \left( \frac{\exp(x_i)}{\sum_j \exp(x_j)}
    \right)

  Args:
    x : input array
    axis: the axis or axes along which the :code:`log_softmax` should be
      computed. Either an integer, tuple of integers, or ``None`` (all axes).
    where: Elements to include in the :code:`log_softmax`. The output for any
      masked-out element is minus infinity.

  Returns:
    An array.

  Note:
    If any input values are ``+inf``, the result will be all ``NaN``: this reflects the
    fact that ``inf / inf`` is not well-defined in the context of floating-point math.

  See also:
    :func:`softmax`
  """
  x_arr = numpy_util.ensure_arraylike("log_softmax", x)
  x_max = jnp.max(x_arr, axis, where=where, initial=-np.inf, keepdims=True)
  x_safe = x_arr if where is None else jnp.where(where, x_arr, -np.inf)
  shifted = x_safe - lax.stop_gradient(x_max)
  shifted_logsumexp = jnp.log(
      jnp.sum(jnp.exp(shifted), axis, where=where, keepdims=True))
  result = shifted - shifted_logsumexp
  if where is not None:
    return jnp.where(where, result, -np.inf)
  return result


def log_softmax(x: ArrayLike,
                /,
                *,
                axis: int | tuple[int, ...] | None = None,
                ) -> Array:
  r"""Log-Softmax function.

  JAX implementation of :func:`scipy.special.log_softmax`

  Computes the logarithm of the :code:`softmax` function, which rescales
  elements to the range :math:`[-\infty, 0)`.

  .. math ::
    \mathrm{log\_softmax}(x)_i = \log \left( \frac{\exp(x_i)}{\sum_j \exp(x_j)}
    \right)

  Args:
    x : input array
    axis: the axis or axes along which the :code:`log_softmax` should be
      computed. ``None`` means all axes.

  Returns:
    An array of the same shape as ``x``

  Note:
    If any input values are ``+inf``, the result will be all ``NaN``: this
    reflects the fact that ``inf / inf`` is not well-defined in the context of
    floating-point math.

  See also:
    :func:`softmax`
  """
  return nn_log_softmax(x, axis=axis)

