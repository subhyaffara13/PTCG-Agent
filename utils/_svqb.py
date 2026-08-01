
def _svqb(X):
  """Derives a truncated orthonormal basis for `X`.

  SVQB [1] is an accelerator-friendly orthonormalization procedure, which
  squares the matrix `C = X.T @ X` and computes an eigenbasis for a smaller
  `(k, k)` system; this offloads most of the work in orthonormalization
  to the first multiply when `n` is large.

  Importantly, if diagonalizing the squared matrix `C` reveals rank deficiency
  of X (which would be evidenced by near-0 then), eigenvalues corresponding
  columns are zeroed out.

  [1]: https://sdm.lbl.gov/~kewu/ps/45577.html

  Args:
    X : An `(n, k)` array which describes a linear subspace of R^n, possibly
        numerically degenerate with some rank less than `k`.

  Returns:
    An orthonormal space `V` described by a `(n, k)` array, with trailing
    columns possibly zeroed out if `X` is of low rank.
  """

  # In [1] diagonal conditioning is explicit, but by normalizing first
  # we can simplify the formulas a bit, since then diagonal conditioning
  # becomes a no-op.
  norms = jnp.linalg.norm(X, ord=2, axis=0, keepdims=True)
  X /= jnp.where(norms == 0, 1.0, norms)

  inner = _mm(X.T, X)

  w, V = _eigh_ascending(inner)

  # All mask logic is used to avoid divide-by-zeros when input columns
  # may have been zero or new zero columns introduced from truncation.
  #
  # If an eigenvalue is less than max eigvalue * eps, then consider
  # that direction "degenerate".
  tau = jnp.finfo(X.dtype).eps * w[0]
  padded = jnp.maximum(w, tau)

  # Note the tau == 0 edge case where X was all zeros.
  sqrted = jnp.where(tau > 0, padded, 1.0) ** (-0.5)

  # X^T X = V diag(w) V^T, so
  # W = X V diag(w)^(-1/2) will yield W^T W = I (excerpting zeros).
  scaledV = V * sqrted[jnp.newaxis, :]
  orthoX = _mm(X, scaledV)

  keep = ((w > tau) * (jnp.diag(inner) > 0.0))[jnp.newaxis, :]
  orthoX *= keep.astype(orthoX.dtype)
  norms = jnp.linalg.norm(orthoX, ord=2, axis=0, keepdims=True)
  keep *= norms > 0.0
  orthoX /= jnp.where(keep, norms, 1.0)
  return orthoX

