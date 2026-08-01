
def _project_out(basis, U):
  """Derives component of U in the orthogonal complement of basis.

  This method iteratively subtracts out the basis component and orthonormalizes
  the remainder. To an extent, these two operations can oppose each other
  when the remainder norm is near-zero (since normalization enlarges a vector
  which may possibly lie in the subspace `basis` to be subtracted).

  We make sure to prioritize orthogonality between `basis` and `U`, favoring
  to return a lower-rank space thank `rank(U)`, in this tradeoff.

  Args:
    basis : An `(n, m)` array which describes a linear subspace of R^n, this
        is assumed to be orthonormal but zero columns are allowed.
    U : An `(n, k)` array representing another subspace of R^n, whose `basis`
        component is to be projected out.

  Returns:
    An `(n, k)` array, with some columns possibly zeroed out, representing
    the component of `U` in the complement of `basis`. The nonzero columns
    are mutually orthonormal.
  """

  # See Sec. 6.9 of The Symmetric Eigenvalue Problem by Beresford Parlett [1]
  # which motivates two loop iterations for basis subtraction. This
  # "twice is enough" approach is due to Kahan. See also a practical note
  # by SLEPc developers [2].
  #
  # Interspersing with orthonormalization isn't directly grounded in the
  # original analysis, but taken from Algorithm 5 of [3]. In practice, due to
  # normalization, I have noticed that the orthonormalized basis
  # does not always end up as a subspace of the starting basis in practice.
  # There may be room to refine this procedure further, but the adjustment
  # in the subsequent block handles this edge case well enough for now.
  #
  # [1]: https://epubs.siam.org/doi/abs/10.1137/1.9781611971163
  # [2]: http://slepc.upv.es/documentation/reports/str1.pdf
  # [3]: https://arxiv.org/abs/1704.07458
  for _ in range(2):
    U -= _mm(basis, _mm(basis.T, U))
    U = _orthonormalize(U)

  # It's crucial to end on a subtraction of the original basis.
  # This seems to be a detail not present in [2], possibly because of
  # of reliance on soft locking.
  #
  # Near convergence, if the residuals R are 0 and our last
  # operation when projecting (X, P) out from R is the orthonormalization
  # done above, then due to catastrophic cancellation we may re-introduce
  # (X, P) subspace components into U, which can ruin the Rayleigh-Ritz
  # conditioning.
  #
  # We zero out any columns that are even remotely suspicious, so the invariant
  # that [basis, U] is zero-or-orthogonal is ensured.
  for _ in range(2):
    U -= _mm(basis, _mm(basis.T, U))
  normU = jnp.linalg.norm(U, ord=2, axis=0, keepdims=True)
  U *= (normU >= 0.99).astype(U.dtype)

  return U

