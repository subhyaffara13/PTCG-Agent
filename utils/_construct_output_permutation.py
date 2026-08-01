
def _construct_output_permutation(
    used: list[tuple[bool, ...]],
) -> list[int]:
  order = []
  for u in used:
    true_vals = [i for i in range(len(u)) if u[i]]
    order.extend(true_vals)
  return [order.index(i) for i in range(len(order))]

