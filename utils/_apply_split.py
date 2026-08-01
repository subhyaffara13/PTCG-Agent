
def _apply_split(
    factors: list[Factor], targets: tuple[int, ...]
) -> list[list[Factor]] | None:
  factors = _consolidate(factors)
  queue = collections.deque(factors)
  result = []

  for i, needed in enumerate(targets):
    new_dim = []
    current_size = 1

    # Consume factors iteratively until the required shape volume is met
    while current_size < needed:
      if not queue:
        return None
      b = queue.popleft()

      # Case A: Perfect match or consume smaller outer block
      if needed % (current_size * b.size) == 0:
        new_dim.append(b)
        current_size *= b.size

      # Case B: Split a larger block (only allowed over logical outer limits)
      elif (current_size * b.size) % needed == 0:
        if b.kind != "outer":
          return None  # Illegal splitting of hardware tile limit
        take = needed // current_size
        new_dim.append(Factor(take, "outer"))
        queue.appendleft(Factor(b.size // take, "outer"))
        current_size *= take
      else:
        return None

    # Sweep any trailing physical size-1 markers exactly into the right-most split dimension
    if i == len(targets) - 1:
      while queue and queue[0].size == 1:
        new_dim.append(queue.popleft())

    result.append(_consolidate(new_dim))

  if queue:
    return None
  return result

