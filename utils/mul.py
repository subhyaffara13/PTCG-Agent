
def mul(a, b):
    both_bool = is_boolean_type(a) and is_boolean_type(b)
    if both_bool:
        return logical_and(a, b)
    else:
        fn = ops_wrapper(aten.mul.__name__)
        return make_pointwise(fn)(a, b)


def mul(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.mul(a, b)


def mul(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._is_bool(self) and symbolic_helper._is_bool(other):
        # ONNX Mul doesn't support Boolean, so use And as an equivalent operator.
        return g.op("And", self, other)
    else:
        return g.op("Mul", self, other)


def mul(*args):
    return reduce(lambda a, b: a * b, args, 1)


def mul(lhs: _ods_ir.Value, rhs: _ods_ir.Value, overflow_flags, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MulOp(lhs=lhs, rhs=rhs, overflowFlags=overflow_flags, results=results, loc=loc, ip=ip).result


def mul(x, y, /, *, out_dtype=None):
  if out_dtype is not None:
    x = np.astype(x, out_dtype)
    y = np.astype(y, out_dtype)
  return np.multiply(x, y)


def mul(x: ArrayLike, y: ArrayLike, *, out_dtype: DTypeLike | None = None
        ) -> Array:
  r"""Elementwise multiplication: :math:`x \times y`.

  This function lowers directly to the `stablehlo.multiply`_ operation.

  Args:
    x, y: Input arrays. Must have matching numerical dtypes. If neither
      is a scalar, ``x`` and ``y`` must have the same number of dimensions
      and be broadcast compatible.
    out_dtype: Optional. Either ``None`` (default), or a dtype. If
      it is a dtype, the output will be of the specified dtype. Typically, this
      is accomplished by casting the inputs to the specified dtype before the
      multiplication is performed, but on some backends this may be done via
      a custom kernel.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the product
    of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.multiply`: NumPy-style multiplication supporting
      inputs with mixed dtypes and ranks.

  .. _stablehlo.multiply: https://openxla.org/stablehlo/spec#multiply
  """
  x, y = core.auto_insert_reshard(x, y)
  return mul_p.bind(x, y, out_dtype=out_dtype)

