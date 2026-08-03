import functools

def _nonempty_prod(arrs: Sequence[Array]) -> Array:
  return functools.reduce(operator.mul, arrs)

