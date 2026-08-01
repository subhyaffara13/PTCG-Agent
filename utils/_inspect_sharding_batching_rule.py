
def _inspect_sharding_batching_rule(args, _, *, callback):
  value, = args
  inspect_sharding_p.bind(value, callback=callback)
  return [], []

