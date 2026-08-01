
def atomic_xchg(x_ref_or_view, idx, val, *, mask: Any | None = None):
  """Atomically exchanges the given value with the value at the given index.

  Args:
    x_ref_or_view: The ref to operate on.
    idx: The indexer to use.
    mask: TO BE DOCUMENTED.

  Returns:
    The value at the given index prior to the aupdate.
  """
  return _atomic_rmw(
      x_ref_or_view, idx, val, mask=mask, atomic_type=AtomicOpType.XCHG
  )

