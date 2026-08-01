
def all_gather_start(*args, **kwargs):
  x = _all_gather_is_async(*args, **kwargs, is_async=True)
  return core.Future(x, all_gather_done_p.bind)

