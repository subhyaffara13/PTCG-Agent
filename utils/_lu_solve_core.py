import math


def _lu_solve_core(lu: Array, permutation: Array, b: Array, trans: int) -> Array:
  m = lu.shape[0]
  x = lax.reshape(b, (m, math.prod(b.shape[1:])))
  if trans == 0:
    x = x[permutation, :]
    x = triangular_solve(lu, x, left_side=True, lower=True, unit_diagonal=True)
    x = triangular_solve(lu, x, left_side=True, lower=False)
  elif trans == 1 or trans == 2:
    conj = trans == 2
    x = triangular_solve(lu, x, left_side=True, lower=False, transpose_a=True,
                         conjugate_a=conj)
    x = triangular_solve(lu, x, left_side=True, lower=True, unit_diagonal=True,
                         transpose_a=True, conjugate_a=conj)
    _, ind = lax.sort_key_val(permutation, lax.iota('int32', permutation.shape[0]))
    x = x[ind, :]
  else:
    raise ValueError(f"'trans' value must be 0, 1, or 2, got {trans}")
  return lax.reshape(x, b.shape)

