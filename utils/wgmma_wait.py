
def wgmma_wait(n: int):
  """Waits until there is no more than ``n`` WGMMA operations in flight."""
  return wgmma_wait_p.bind(n)

