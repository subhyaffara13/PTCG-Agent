
def _flatten_defaultdict_with_keys(d):
  keys = tuple(sorted(d))
  return tuple((DictKey(k), d[k]) for k in keys), (d.default_factory, keys)

