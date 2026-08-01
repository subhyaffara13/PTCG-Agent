
def wait_load_tmem():
  """Awaits all previously asynchronous TMEM loads issued by the calling thread.

  Once this function returns, the TMEM loads issued by the calling thread are
  guaranteed to have completed. The read TMEM regions can be safely overwritten
  by the calling thread, or any threads signalled through ``Barrier``s with
  ``orders_tensor_core=True``.
  """
  wait_load_tmem_p.bind()


def wait_load_tmem() -> None:
  nvvm.tcgen05_wait(nvvm.Tcgen05WaitKind.LOAD)
  utils.warpgroup_barrier()

