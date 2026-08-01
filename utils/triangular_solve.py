
def triangular_solve(a: _ods_ir.Value[_ods_ir.RankedTensorType], b: _ods_ir.Value[_ods_ir.RankedTensorType], left_side: _Union[bool, _ods_ir.BoolAttr], lower: _Union[bool, _ods_ir.BoolAttr], unit_diagonal: _Union[bool, _ods_ir.BoolAttr], transpose_a: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TriangularSolveOp(a=a, b=b, left_side=left_side, lower=lower, unit_diagonal=unit_diagonal, transpose_a=transpose_a, results=results, loc=loc, ip=ip).result


def triangular_solve(a: _ods_ir.Value[_ods_ir.RankedTensorType], b: _ods_ir.Value[_ods_ir.RankedTensorType], left_side: _Union[bool, _ods_ir.BoolAttr], lower: _Union[bool, _ods_ir.BoolAttr], unit_diagonal: _Union[bool, _ods_ir.BoolAttr], transpose_a: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TriangularSolveOp(a=a, b=b, left_side=left_side, lower=lower, unit_diagonal=unit_diagonal, transpose_a=transpose_a, results=results, loc=loc, ip=ip).result


def triangular_solve(
    a: ArrayLike,
    b: ArrayLike,
    *,
    left_side: bool = False,
    lower: bool = False,
    transpose_a: bool = False,
    conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> Array:
  r"""Triangular solve.

  Solves either the matrix equation

  .. math::
    \mathit{op}(A) . X = B

  if ``left_side`` is ``True`` or

  .. math::
    X . \mathit{op}(A) = B

  if ``left_side`` is ``False``.

  ``A`` must be a lower or upper triangular square matrix, and where
  :math:`\mathit{op}(A)` may either transpose :math:`A` if ``transpose_a``
  is ``True`` and/or take its complex conjugate if ``conjugate_a`` is ``True``.

  Args:
    a: A batch of matrices with shape ``[..., m, m]``.
    b: A batch of matrices with shape ``[..., m, n]`` if ``left_side`` is
      ``True`` or shape ``[..., n, m]`` otherwise.
    left_side: describes which of the two matrix equations to solve; see above.
    lower: describes which triangle of ``a`` should be used. The other triangle
      is ignored.
    transpose_a: if ``True``, the value of ``a`` is transposed.
    conjugate_a: if ``True``, the complex conjugate of ``a`` is used in the
      solve. Has no effect if ``a`` is real.
    unit_diagonal: if ``True``, the diagonal of ``a`` is assumed to be unit
      (all 1s) and not accessed.

  Returns:
    A batch of matrices the same shape and dtype as ``b``.
  """
  conjugate_a = conjugate_a and dtypes.issubdtype(lax.dtype(a), np.complexfloating)
  singleton = np.ndim(b) == np.ndim(a) - 1
  if singleton:
    b = lax.expand_dims(b, (-1 if left_side else -2,))
  a, b = core.auto_insert_reshard(a, b)
  out = triangular_solve_p.bind(
      a, b, left_side=left_side, lower=lower, transpose_a=transpose_a,
      conjugate_a=conjugate_a, unit_diagonal=unit_diagonal)
  if singleton:
    out = out[..., 0] if left_side else out[..., 0, :]
  return out

