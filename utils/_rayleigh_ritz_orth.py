
def _rayleigh_ritz_orth(A, S):
  """Solve the Rayleigh-Ritz problem for `A` projected to `S`.

  Solves the local eigenproblem for `A` within the subspace `S`, which is
  assumed to be orthonormal (with zero columns allowed), identifying `w, V`
  satisfying

  (1) `S.T A S V ~= diag(w) V`
  (2) `V` is standard orthonormal

  Note that (2) is simplified to be standard orthonormal because `S` is.

  Args:
    A: An operator representing the action of an `n`-sized square matrix.
    S: An orthonormal subspace of R^n represented by an `(n, k)` array, with
       zero columns allowed.

  Returns:
    Eigenvectors `V` and eigenvalues `w` satisfying the size-`k` system
    described in this method doc. Note `V` will be full rank, even if `S` isn't.
  """

  SAS = _mm(S.T, A(S))

  # Solve the projected subsystem.
  # If we could tell to eigh to stop after first k, we would.
  return _eigh_ascending(SAS)

