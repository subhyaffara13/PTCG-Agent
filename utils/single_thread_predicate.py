
def single_thread_predicate(scope: ThreadSubset = ThreadSubset.BLOCK):
  """Returns a predicate that selects a single thread.

  Args:
    scope: What level of the thread hierarchy to select a thread from. For
      example, if the scope is BLOCK, only one thread per block will be
      selected.
  """
  elected = nvvm.elect_sync()
  if scope == ThreadSubset.WARP:
    return elected
  warp = warp_idx()
  if scope is not ThreadSubset.BLOCK:
    warp = arith.remui(warp, c(4, warp.type))
  first_warp = arith.cmpi(arith.CmpIPredicate.eq, warp, c(0, warp.type))
  return arith.andi(first_warp, elected)

