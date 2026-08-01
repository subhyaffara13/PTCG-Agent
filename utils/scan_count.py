
def scan_count(in_mask: _ods_ir.Value[_ods_ir.VectorType], values: _ods_ir.Value[_ods_ir.VectorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return ScanCountOp(in_mask=in_mask, values=values, results=results, loc=loc, ip=ip).results


def scan_count(
    x: jax.Array, mask: jax.Array | None = None
) -> tuple[jax.Array, jax.Array]:
  """Computes the running duplicate occurrence count of the array.

  Args:
    x: An array of integers or floats.
    mask: An optional array of booleans, which specifies which elements ``x``
      are eligible for counting. If ``None``, all elements are eligible.

  Returns:
    A tuple of two arrays:

      * the running duplicate occurrence count of ``x``;
      * the mask indicating the last occurrence of each duplicate that was
        counted.
  """
  return scan_count_p.bind(x, lax.full(x.shape, True) if mask is None else mask)

