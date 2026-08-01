
def atomic_or(ref: _Ref, val) -> None:
  """Performs an atomic store-or of the value to the reference.

  Note that atomicity is only guaranteed on the element-level.

  Args:
    ref: The reference to store the value to.
    val: The value to store.
  """
  _atomic_store(ref, val, atomic_type=AtomicOpType.OR)


def atomic_or(x_ref_or_view, idx, val, *, mask: Any | None = None):
  """Atomically computes ``x_ref_or_view[idx] |= val``.

  Args:
    x_ref_or_view: The ref to operate on.
    idx: The indexer to use.
    mask: TO BE DOCUMENTED.

  Returns:
    The value at the given index prior to the atomic operation.
  """
  return _atomic_rmw(
      x_ref_or_view, idx, val, mask=mask, atomic_type=AtomicOpType.OR
  )

