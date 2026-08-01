
def psum_start(*args, **kwargs):
  x = _psum_is_async(*args, **kwargs, is_async=True)
  return core.Future(x, psum_done_p.bind)

