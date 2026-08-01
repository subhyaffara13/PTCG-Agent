
def _fix_fwd_args(f, *args):
  args = [(x, True) for x in args]
  args = [x for pair in args for x in pair]
  return f(*args)

