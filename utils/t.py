import random

def t(self: list[int]):
    if len(self) > 2:
        raise AssertionError(
            f"Expected tensor to have <= 2 dimensions, but got {len(self)}"
        )
    self_len = len(self)
    if self_len == 0:
        out: list[int] = []
        return out
    elif self_len == 1:
        return [self[0]]
    else:
        return [self[1], self[0]]


def t(a: TensorLikeType):
    # TODO: Add sparse support
    # if a.is_sparse:
    #     sparse_dim = a.sparse_dim()
    #     dense_dim = a.dense_dim()
    #     if not (sparse_dim <= 2 and dense_dim == 0):
    #         raise RuntimeError(
    #             f"t() expects a tensor with <= 2 sparse and 0 dense dimensions, but got {sparse_dim} sparse and"
    #             f"{dense_dim} dense dimensions"
    #         )
    if a.ndim > 2:
        raise RuntimeError(
            f"t() expects a tensor with <= 2 dimensions, but self is {a.ndim}D"
        )
    return torch.transpose(a, 0, 0 if a.ndim < 2 else 1)


def T(a: TensorLikeType) -> TensorLikeType:
    # n != 2 && n != 0 is deprecated in regular PyTorch.
    torch._check(
        a.ndim in (0, 2),
        lambda: (
            "The use of `x.T` on tensors of dimension other than 0 or 2 "
            "to reverse their shape is not supported."
        ),
    )
    return a.t()


def t(g: jit_utils.GraphContext, self):
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is None or rank < 2:
        # The transpose of a 1d or 0d tensor is itself. ONNX does not define the behavior
        # clearly and onnxruntime fails on these cases. So we add an Identity node to
        # mirror the behavior of eager mode.
        return g.op("Identity", self)
    return g.op("Transpose", self, perm_i=(1, 0))


def t(f, *args, **kwds):
    """call one function and check if global RNG changed"""
    global progress
    progress += 1
    print(progress, ",", end="")

    f(*args, **kwds)

    after_np_rv = np.random.rand()
    # if np_rv != after_np_rv:
    #    print(np_rv, after_np_rv, "don't match np!")
    assert np_rv == after_np_rv
    np.random.seed(42)

    after_py_rv = random.random()
    # if py_rv != after_py_rv:
    #    print(py_rv, after_py_rv, "don't match py!")
    assert py_rv == after_py_rv
    random.seed(42)


def t(key: ArrayLike,
      df: RealArray,
      shape: Shape | None = None,
      dtype: DTypeLikeFloat | None = None,
      *,
      out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Student's t random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(t; \nu) \propto \left(1 + \frac{t^2}{\nu}\right)^{-(\nu + 1)/2}

  Where :math:`\nu > 0` is the degrees of freedom, given by the parameter ``df``.

  Args:
    key: a PRNG key used as the random key.
    df: a float or array of floats broadcast-compatible with ``shape``
      representing the degrees of freedom parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``df``. The default (None)
      produces a result shape equal to ``df.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``df.shape``.
  """
  key, _ = _check_prng_key("t", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `t` must be a float "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("t", shape, df)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "t", shape)
  _check_all_safe_to_cast("t", dtype, df)
  return maybe_auto_axes(_t, out_sharding,
                         shape=shape, dtype=dtype)(key, df)

