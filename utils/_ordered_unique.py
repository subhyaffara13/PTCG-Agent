
def _ordered_unique(xs):
  d = collections.OrderedDict((x, None) for x in xs)
  return list(d.keys())

