
def psum_scatter_start(*args, **kwargs):
  x = _psum_scatter_is_async(*args, **kwargs, is_async=True)
  return core.Future(x, reduce_scatter_done_p.bind)

