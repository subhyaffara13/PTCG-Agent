
def single_thread(scope: ThreadSubset = ThreadSubset.BLOCK):
  """Runs the context only from a single thread.

  Args:
    scope: What level of the thread hierarchy to select a thread from. For
      example, if the scope is BLOCK, only one thread per block will be
      selected.
  """
  global _ONCE_PER
  # If we're already in a single-thread context, we don't have to do anything.
  if _ONCE_PER is not None and _ONCE_PER >= scope:
    yield
    return

  prev_scope = _ONCE_PER
  _ONCE_PER = scope
  try:
    if_op = scf.IfOp(single_thread_predicate(scope))
    with ir.InsertionPoint(if_op.then_block):
      yield
      scf.YieldOp([])
  finally:
    _ONCE_PER = prev_scope

