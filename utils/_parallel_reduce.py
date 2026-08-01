
def _parallel_reduce(
    sequence: list[T],
    operation: Callable[[T, T], T],
    identity: T | Unspecified = Unspecified(),
) -> T:
  length = len(sequence)
  if length == 0:
    if isinstance(identity, Unspecified):
      raise TypeError("Must specify identity for parallel reduction of empty sequence.")
    return identity
  elif length == 1:
    return sequence[0]
  else:
    index = length // 2
    a = _parallel_reduce(sequence[:index], operation, identity)
    b = _parallel_reduce(sequence[index:], operation, identity)
    return operation(a, b)

