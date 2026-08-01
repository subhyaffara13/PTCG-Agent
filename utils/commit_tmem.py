
def commit_tmem():
  """Commits all writes to TMEM issued by the current thread.

  Once this function returns, the effects of calling ``async_store_tmem`` from
  the current thread are visible to TMEM loads, MMA and barrier operations of
  ``Barrier``s with ``orders_tensor_core=True``.
  """
  commit_tmem_p.bind()


def commit_tmem() -> None:
  nvvm.tcgen05_wait(nvvm.Tcgen05WaitKind.STORE)
  utils.warpgroup_barrier()

