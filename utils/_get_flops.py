
def _get_flops(fn, *args, **kwargs):
  e = jax.jit(fn).lower(*args, **kwargs)
  cost = e.cost_analysis()
  if cost is None:
    return 0
  flops = int(cost['flops']) if 'flops' in cost else 0
  return flops


def _get_flops(e) -> int:
  cost = e.cost_analysis() or e.compile().cost_analysis()
  return 0 if cost is None or 'flops' not in cost else int(cost['flops'])

