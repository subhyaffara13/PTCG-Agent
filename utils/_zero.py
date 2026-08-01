
def _zero(x):
  x_aval = core.typeof(x)
  out = full_like(x, shape=(), fill_value=0,
                  sharding=x_aval.sharding.update(spec=P()))
  return out

