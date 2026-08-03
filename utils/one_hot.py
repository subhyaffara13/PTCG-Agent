from typing import Any

def one_hot(x: torch.Tensor, v_bins: torch.Tensor) -> torch.Tensor:
    reshaped_bins = v_bins.view(((1,) * len(x.shape)) + (len(v_bins),))
    diffs = x[..., None] - reshaped_bins
    am = torch.argmin(torch.abs(diffs), dim=-1)
    return nn.functional.one_hot(am, num_classes=len(v_bins)).float()


def one_hot(self: Tensor, num_classes: int = -1) -> Tensor:
    if num_classes == -1:
        num_classes = int(self.max().item()) + 1
    # _assert_async is side-effectful and won't be DCE'd
    aten._assert_async.msg(
        torch.all(self >= 0),
        "one_hot: Class values must be non-negative.",
    )
    aten._assert_async.msg(
        torch.all(self < num_classes),
        "one_hot: Class values must be smaller than num_classes.",
    )
    return (
        self.unsqueeze(-1)
        == torch.arange(num_classes, dtype=self.dtype, device=self.device)
    ).to(torch.int64)


def one_hot(g: jit_utils.GraphContext, self, num_classes):
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    # onnxruntime supports limited type combinations for OneHot.
    if _type_utils.JitScalarType.from_value(
        num_classes, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.UINT8,
        _type_utils.JitScalarType.INT8,
        _type_utils.JitScalarType.INT,
        _type_utils.JitScalarType.INT16,
    }:
        num_classes = g.op("Cast", num_classes, to_i=_C_onnx.TensorProtoDataType.INT64)
    return g.op("OneHot", self, num_classes, values, axis_i=-1)


def one_hot(
    x: Array,
    /,
    num_classes: int,
    *,
    dtype: DType | None = None,
    axis: int = -1,
    xp: ModuleType | None = None,
) -> Array:
    """
    One-hot encode the given indices.

    Each index in the input `x` is encoded as a vector of zeros of length `num_classes`
    with the element at the given index set to one.

    Parameters
    ----------
    x : array
        An array with integral dtype whose values are between `0` and `num_classes - 1`.
    num_classes : int
        Number of classes in the one-hot dimension.
    dtype : DType, optional
        The dtype of the return value.  Defaults to the default float dtype (usually
        float64).
    axis : int, optional
        Position in the expanded axes where the new axis is placed. Default: -1.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        An array having the same shape as `x` except for a new axis at the position
        given by `axis` having size `num_classes`.  If `axis` is unspecified, it
        defaults to -1, which appends a new axis.

        If ``x < 0`` or ``x >= num_classes``, then the result is undefined, may raise
        an exception, or may even cause a bad state.  `x` is not checked.

    Examples
    --------
    >>> import array_api_extra as xpx
    >>> import array_api_strict as xp
    >>> xpx.one_hot(xp.asarray([1, 2, 0]), 3)
    Array([[0., 1., 0.],
          [0., 0., 1.],
          [1., 0., 0.]], dtype=array_api_strict.float64)
    """
    # Validate inputs.
    if xp is None:
        xp = array_namespace(x)
    if not xp.isdtype(x.dtype, "integral"):
        msg = "x must have an integral dtype."
        raise TypeError(msg)
    if dtype is None:
        dtype = _funcs.default_dtype(xp, device=get_device(x))
    # Delegate where possible.
    if is_jax_namespace(xp):
        from jax.nn import one_hot as jax_one_hot

        return jax_one_hot(x, num_classes, dtype=dtype, axis=axis)
    if is_torch_namespace(xp):
        from torch.nn.functional import one_hot as torch_one_hot

        x = xp.astype(x, xp.int64)  # PyTorch only supports int64 here.
        try:
            out = torch_one_hot(x, num_classes)
        except RuntimeError as e:
            raise IndexError from e
    else:
        out = _funcs.one_hot(x, num_classes, xp=xp)
    out = xp.astype(out, dtype, copy=False)
    if axis != -1:
        out = xp.moveaxis(out, -1, axis)
    return out


def one_hot(
    x: Array,
    /,
    num_classes: int,
    *,
    xp: ModuleType,
) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in `array_api_extra._delegation.py`."""
    # TODO: Benchmark whether this is faster on the NumPy backend:
    # if is_numpy_array(x):
    #     out = xp.zeros((x.size, num_classes), dtype=dtype)
    #     out[xp.arange(x.size), xp.reshape(x, (-1,))] = 1
    #     return xp.reshape(out, (*x.shape, num_classes))
    range_num_classes = xp.arange(num_classes, dtype=x.dtype, device=_compat.device(x))
    return x[..., xp.newaxis] == range_num_classes


def one_hot(x, k):
  """Returns a one-hot encoding of `x` of size `k`."""
  return jnp.array(x[..., jnp.newaxis] == jnp.arange(k), dtype=np.float32)


def one_hot(x, k):
  """Returns a one-hot encoding of `x` of size `k`."""
  return jnp.array(x[..., jnp.newaxis] == jnp.arange(k), dtype=np.float32)


def one_hot(x: Any, num_classes: int, *,
            dtype: Any | None = None, axis: int | AxisName = -1) -> Array:
  r"""One-hot encodes the given indices.

  Each index in the input ``x`` is encoded as a vector of zeros of length
  ``num_classes`` with the element at ``index`` set to one::

    >>> jax.nn.one_hot(jnp.array([0, 1, 2]), 3)
    Array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]], dtype=float32)

  Indices outside the range :math:`[0, \text{num\_classes})` will be encoded as zeros::

    >>> jax.nn.one_hot(jnp.array([-1, 3]), 3)
    Array([[0., 0., 0.],
           [0., 0., 0.]], dtype=float32)

  Args:
    x: A tensor of indices.
    num_classes: Number of classes in the one-hot dimension.
    dtype: optional, a float dtype for the returned values (default :obj:`jnp.float_`).
    axis: the axis or axes along which the function should be
      computed.
  """
  num_classes = core.concrete_dim_or_error(
      num_classes,
      "The error arose in jax.nn.one_hot argument `num_classes`.")
  x_arr = jnp.asarray(x)
  if not dtypes.isdtype(x_arr.dtype, "integral"):
    # Deprecated 2024-12-18
    deprecations.warn(
      'jax-nn-one-hot-float-input',
      f"jax.nn.one_hot input should be integer-typed; got dtype={x_arr.dtype}",
      stacklevel=1)
  dtype = dtypes.default_float_dtype() if dtype is None else dtype
  return _one_hot(x_arr, num_classes, dtype=dtype, axis=axis)

