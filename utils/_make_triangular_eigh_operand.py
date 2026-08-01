
def _make_triangular_eigh_operand(shape, dtype, lower: bool, rng: Rng):
  # For testing eigh we use triangular matrices
  operand = jtu.rand_default(rng)(shape, dtype)
  # Make operand self-adjoint
  operand = (operand + np.conj(np.swapaxes(operand, -1, -2))) / 2
  # Make operand lower/upper triangular
  return operand  # np.tril(operand) if lower else np.triu(operand)

