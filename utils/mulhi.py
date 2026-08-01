
def mulhi(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MulhiOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def mulhi(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MulhiOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def mulhi(x, y):
  x = np.asarray(x)
  y = np.asarray(y)
  dtype = x.dtype
  if not np.issubdtype(dtype, np.integer):
    raise TypeError(f'mulhi requires integer inputs, got {dtype}')
  if dtype != y.dtype:
    raise TypeError(
        f'mulhi operands must have the same dtype, got {dtype} and {y.dtype}'
    )
  info = np.iinfo(dtype)
  bits = info.bits
  is_signed = np.issubdtype(dtype, np.signedinteger)
  # For 64-bit inputs, use Python object dtype for arbitrary precision.
  if bits == 64:
    widen_dtype = np.dtype(object)
  else:
    widen_bits = bits * 2
    widen_dtype = np.dtype(f'{"i" if is_signed else "u"}{widen_bits // 8}')
  prod = x.astype(widen_dtype) * y.astype(widen_dtype)
  return (prod >> bits).astype(dtype)


def mulhi(x: ArrayLike, y: ArrayLike, /) -> Array:
  r"""Elementwise multiply-high: high bits of :math:`x \times y`.

  For N-bit integer inputs, this function computes the upper N bits of
  the full 2N-bit product.

  Args:
    x, y: Input arrays. Must have an integer dtype. If neither is a
      scalar, ``x`` and ``y`` must have the same number of dimensions and be
      broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the most
    significant N bits of the 2N-bit product of each pair of broadcasted
    entries.
  """
  x, y = core.auto_insert_reshard(x, y)
  return mulhi_p.bind(x, y)

