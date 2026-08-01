
def ppermute_start(*args, **kwargs):
  x = _ppermute_is_async(*args, **kwargs, is_async=True)
  return core.Future(x, ppermute_done_p.bind)

