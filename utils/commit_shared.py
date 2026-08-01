
def commit_shared():
  nvvm.fence_proxy(
      nvvm.ProxyKind.async_shared, space=nvvm.SharedSpace.shared_cta
  )
  warpgroup_barrier()

