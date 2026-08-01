
def lu_pivots_to_permutation(pivots: ArrayLike, permutation_size: int) -> Array:
  """Converts the pivots (row swaps) returned by LU to a permutation.

  We build a permutation rather than applying `pivots` directly to the rows
  of a matrix because lax loops aren't differentiable.

  Args:
    pivots: an int32 array of shape (..., k) of row swaps to perform
    permutation_size: the size of the output permutation. Has to be >= k.

  Returns:
    An int32 array of shape (..., permutation_size).
  """
  return lu_pivots_to_permutation_p.bind(
      pivots, permutation_size=permutation_size)

