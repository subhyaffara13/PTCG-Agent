
def cumlogsumexp(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative logsumexp along `axis`."""
  return cumlogsumexp_p.bind(operand, axis=int(axis), reverse=bool(reverse))

