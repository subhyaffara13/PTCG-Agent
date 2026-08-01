
def _apply_givens_rotations(H_row, givens, k):
  """
  Applies the Givens rotations stored in the vectors cs and sn to the vector
  H_row. Then constructs and applies a new Givens rotation that eliminates
  H_row's k'th element.
  """
  # This call successively applies each of the
  # Givens rotations stored in givens[:, :k] to H_col.

  def apply_ith_rotation(i, H_row):
    return _rotate_vectors(H_row, i, *givens[i, :])
  R_row = lax.fori_loop(0, k, apply_ith_rotation, H_row)

  givens_factors = _givens_rotation(R_row[k], R_row[k + 1])
  givens = givens.at[k, :].set(givens_factors)
  R_row = _rotate_vectors(R_row, k, *givens_factors)
  return R_row, givens

