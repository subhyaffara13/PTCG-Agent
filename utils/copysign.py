
def copysign(a: TensorLikeType | NumberType, b: TensorLikeType | NumberType):
    if isinstance(b, Number) and isinstance(a, Tensor):
        # pyrefly: ignore [bad-argument-type]
        b = scalar_tensor(b, dtype=a.dtype, device=a.device)
    elif isinstance(a, Tensor) and isinstance(b, Tensor) and a.device != b.device:
        msg = f"Expected divisor (b) to be on the same device ({a.device}) as dividend (a), but it is found on {b.device}!"
        raise RuntimeError(msg)
    # pyrefly: ignore [bad-argument-type]
    return where(signbit(b), neg(abs(a)), abs(a))


def copysign(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CopySignOp(lhs=lhs, rhs=rhs, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def copysign(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Copies the sign of each element in ``x2`` to the corresponding element in ``x1``.

  JAX implementation of :obj:`numpy.copysign`.

  Args:
    x1: Input array
    x2: The array whose elements will be used to determine the sign, must be
      broadcast-compatible with ``x1``

  Returns:
    An array object containing the potentially changed elements of ``x1``, always promotes
    to inexact dtype, and has a shape of ``jnp.broadcast_shapes(x1.shape, x2.shape)``

  Examples:
    >>> x1 = jnp.array([5, 2, 0])
    >>> x2 = -1
    >>> jnp.copysign(x1, x2)
    Array([-5., -2., -0.], dtype=float32)

    >>> x1 = jnp.array([6, 8, 0])
    >>> x2 = 2
    >>> jnp.copysign(x1, x2)
    Array([6., 8., 0.], dtype=float32)

    >>> x1 = jnp.array([2, -3])
    >>> x2 = jnp.array([[1],[-4], [5]])
    >>> jnp.copysign(x1, x2)
    Array([[ 2.,  3.],
           [-2., -3.],
           [ 2.,  3.]], dtype=float32)
  """
  x1, x2 = promote_args_inexact("copysign", x1, x2)
  if dtypes.issubdtype(x1.dtype, np.complexfloating):
    raise TypeError("copysign does not support complex-valued inputs")
  return _where(signbit(x2).astype(bool), -lax.abs(x1), lax.abs(x1))

