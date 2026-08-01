
def _extend_basis(X, m):
  """Extend the basis of `X` with `m` addition dimensions.

  Given an orthonormal `X` of dimension `k`, a typical strategy for deriving
  an extended basis is to generate a random one and project it out.

  We instead generate a basis using block householder reflectors [1] [2] to
  leverage the favorable properties of determinism and avoiding the chance that
  the generated random basis has overlap with the starting basis, which may
  happen with non-negligible probability in low-dimensional cases.

  [1]: https://epubs.siam.org/doi/abs/10.1137/0725014
  [2]: https://www.jstage.jst.go.jp/article/ipsjdc/2/0/2_0_298/_article

  Args:
    X : An `(n, k)` array representing a `k`-rank orthonormal basis for a linear
        subspace of R^n.
    m : A nonnegative integer such that `k + m <= n` telling us how much to
        extend the basis by.

  Returns:
    An `(n, m)` array representing an extension to the basis of `X` such that
    their union is orthonormal.
  """
  n, k = X.shape
  # X = vstack(Xupper, Xlower), where Xupper is (k, k)
  Xupper, Xlower = jnp.split(X, [k], axis=0)
  u, s, vt = jnp.linalg.svd(Xupper)

  # Adding U V^T to Xupper won't change its row or column space, but notice
  # its singular values are all lifted by 1; we could write its upper k rows
  # as u diag(1 + s) vt.
  y = jnp.concatenate([Xupper + _mm(u, vt), Xlower], axis=0)

  # Suppose we found a full-rank (n, k) matrix w which defines the
  # perpendicular to a space we'd like to reflect over. The block householder
  # reflector H(w) would have the usual involution property.
  #
  # Consider the two definitions below:
  # H(w) = I - 2 w w^T
  # 2 w w^T = y (v diag(1+s)^(-1) vt) y^T
  #
  # After some algebra, we see H(w) X = vstack(-u vt, 0)
  # Applying H(w) to both sides since H(w)^2 = I we have
  # X = H(w) vstack(-u vt, 0). But since H(w) is unitary its action must
  # preserve rank. Thus H(w) vstack(0, eye(n - k)) must be orthogonal to
  # X; taking just the first m columns H(w) vstack(0, eye(m), 0) yields
  # an orthogonal extension to X.
  other = jnp.concatenate(
      [jnp.eye(m, dtype=X.dtype),
       jnp.zeros((n - k - m, m), dtype=X.dtype)], axis=0)
  w = _mm(y, vt.T * ((2 * (1 + s)) ** (-1/2))[jnp.newaxis, :])
  h = -2 * jnp.linalg.multi_dot(
      [w, w[k:, :].T, other], precision=jax.lax.Precision.HIGHEST)
  return h.at[k:].add(other)

