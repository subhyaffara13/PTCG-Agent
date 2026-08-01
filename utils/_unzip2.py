
def _unzip2(xs):
  ys = tuple(zip(*xs))
  return ys if ys else ((), ())

