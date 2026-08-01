
def _sum_tangents(_, x, *xs):
  return reduce(ad.add_tangents, xs, x)

