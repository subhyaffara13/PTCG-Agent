
def _interleave_fun(f, every_others, *args, **kwargs):
  args_ = [x for pair in zip(args, every_others) for x in pair]
  return f(*args_, **kwargs)

