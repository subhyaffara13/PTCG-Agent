
def _lu_pivots_body_fn_inner(i, permutation, swaps):
  j = swaps[i]
  x = permutation[i]
  y = permutation[j]
  permutation = permutation.at[i].set(y)
  return permutation.at[j].set(x)

