
def _concatenate_tree(xs, dimension: int):
  # concatenate can be slow to compile for wide concatenations, so form a
  # tree of concatenations as a workaround especially for op-by-op mode.
  # (https://github.com/jax-ml/jax/issues/653).
  k = 16
  current_xs = list(xs)
  dimension_attr = mlir.i64_attr(dimension)
  while len(current_xs) > 1:
    current_xs = [hlo.concatenate(current_xs[i:i+k], dimension_attr)
                  for i in range(0, len(current_xs), k)]
  return current_xs[0]

