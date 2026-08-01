
def linen_rngs_dict(linen_module: linen.Module, add_default: bool = False):
  """Given a module, split out one of its every active RNG key collections."""
  assert linen_module.scope is not None, 'linen_rngs_dict() must be called inside a Linen module.'
  rngs: dict[str, tp.Any] = {
      name: linen_module.make_rng(name)
      for name in linen_module.scope.rngs.keys()
  }
  if add_default and 'default' not in rngs:
    rngs['default'] = 0
  return rngs

