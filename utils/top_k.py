
def top_k(operand: _ods_ir.Value, k: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return TopKOp(operand=operand, k=k, results=results, loc=loc, ip=ip).results


def top_k(operand, k, axis=-1):
  if axis < 0:
    axis = operand.ndim + axis
  assert 0 <= axis < operand.ndim
  operand_flipped = np.flip(operand, axis)
  indices_flipped = np.argsort(operand_flipped, axis=axis, kind="stable")
  indices_all = (operand.shape[axis] - 1 - np.flip(indices_flipped, axis)).astype(np.int32)
  indices = indices_all[(_slice(None),) * axis + (_slice(k),)]
  values = np.take_along_axis(operand, indices, axis=axis)
  return values, indices


def top_k(operand: ArrayLike, k: int, *, axis: int = -1) -> tuple[Array, Array]:
  """Returns top ``k`` values and their indices along the specified axis of ``operand``.

  Args:
    operand: N-dimensional array of non-complex type.
    k: integer specifying the number of top entries.
    axis: optional integer specifying the axis along which to compute the top
      ``k`` entries. Default is -1, indicating the last axis.

  Returns:
    A tuple ``(values, indices)`` where

    - ``values`` is an array containing the top k values along the last axis.
    - ``indices`` is an array containing the indices corresponding to values.

  ``values[..., i, ...]`` is the ``i``-th largest entry in ``operand`` along the
  specified axis, and its index is ``indices[..., i, ...]``.

  If two elements are equal, the lower-index element appears first.

  See also:
    - :func:`jax.lax.approx_max_k`
    - :func:`jax.lax.approx_min_k`

  Examples:
    Find the largest three values, and their indices, within an array:

    >>> x = jnp.array([9., 3., 6., 4., 10.])
    >>> values, indices = jax.lax.top_k(x, 3)
    >>> values
    Array([10.,  9.,  6.], dtype=float32)
    >>> indices
    Array([4, 0, 2], dtype=int32)
  """
  if core.is_constant_dim(k):
    k = int(k)
  if k < 0:
    raise ValueError(f"k argument to top_k must be nonnegative, got {k}")
  axis = canonicalize_axis(axis, np.ndim(operand))
  return top_k_p.bind(operand, k=k, axis=axis)

