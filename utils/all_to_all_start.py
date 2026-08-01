
def all_to_all_start(*args, **kwargs):
  x = _all_to_all_is_async(*args, **kwargs, is_async=True)
  return core.Future(x, all_to_all_done_p.bind)

