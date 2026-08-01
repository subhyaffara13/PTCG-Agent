
def iterated_vmap_unary(n, f):
  for _ in range(n):
    f = api.vmap(f)
  return f

