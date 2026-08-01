
def _lobpcg_standard_callable(
    A: Callable[[jax.Array], jax.Array],
    X: jax.Array,
    m: int,
    tol: jax.Array | float | None,
    debug: bool = False):
  """Supports generic lobpcg_standard() callable interface."""

  # TODO(vladf): support mixed_precision flag, which allows f64 Rayleigh-Ritz
  # with f32 inputs.

  n, k = X.shape
  dt = X.dtype

  _check_inputs(A, X)

  if tol is None:
    tol = float(jnp.finfo(dt).eps)

  X = _orthonormalize(X)
  P = _extend_basis(X, X.shape[1])

  # We maintain X, our current list of best eigenvectors,
  # P, our search direction, and
  # R, our residuals, in a large joint array XPR, column-stacked, so (n, 3*k).

  AX = A(X)
  theta = jnp.sum(X * AX, axis=0, keepdims=True)
  R = AX - theta * X

  def cond(state):
    i, _X, _P, _R, converged, _ = state
    return jnp.logical_and(i < m, converged < k)

  def body(state):
    i, X, P, R, _, theta = state
    # Invariants: X, P, R kept orthonormal
    # Some R, P columns may be 0 (due to basis truncation, as decided
    # by orthogonalization routines), but not X.

    # TODO(vladf): support preconditioning for bottom-k eigenvectors
    # if M is not None:
    #   R = M(R)

    # Residual basis selection.
    R = _project_out(jnp.concatenate((X, P), axis=1), R)
    XPR = jnp.concatenate((X, P, R), axis=1)

    # Projected eigensolve.
    theta, Q = _rayleigh_ritz_orth(A, XPR)

    # Eigenvector X extraction
    B = Q[:, :k]
    normB = jnp.linalg.norm(B, ord=2, axis=0, keepdims=True)
    B /= normB
    X = _mm(XPR, B)
    normX = jnp.linalg.norm(X, ord=2, axis=0, keepdims=True)
    X /= normX

    # Difference terms P extraction
    #
    # In next step of LOBPCG, naively, we'd set
    # P = S[:, k:] @ Q[k:, :k] to achieve span(X, P) == span(X, previous X)
    # (this is not obvious, see section 4 of [1]).
    #
    # Instead we orthogonalize concat(0, Q[k:, :k]) against Q[:, :k]
    # in the standard basis before mapping with XPR. Since XPR is itself
    # orthonormal, the resulting directions are themselves orthonormalized.
    #
    # [2] leverages Q's existing orthogonality to derive
    # an analytic expression for this value based on the quadrant Q[:k,k:]
    # (see section 4.2 of [2]).
    q, _ = jnp.linalg.qr(Q[:k, k:].T)
    diff_rayleigh_ortho = _mm(Q[:, k:], q)
    P = _mm(XPR, diff_rayleigh_ortho)
    normP = jnp.linalg.norm(P, ord=2, axis=0, keepdims=True)
    P /= jnp.where(normP == 0, 1.0, normP)

    # Compute new residuals.
    AX = A(X)
    R = AX - theta[jnp.newaxis, :k] * X
    resid_norms = jnp.linalg.norm(R, ord=2, axis=0)

    # I tried many variants of hard and soft locking [3]. All of them seemed
    # to worsen performance relative to no locking.
    #
    # Further, I found a more experimental convergence formula compared to what
    # is suggested in the literature, loosely based on floating-point
    # expectations.
    #
    # [2] discusses various strategies for this in Sec 5.3. The solution
    # they end up with, which estimates operator norm |A| via Gaussian
    # products, was too crude in practice (and overly-lax). The Gaussian
    # approximation seems like an estimate of the average eigenvalue.
    #
    # Instead, we test convergence via self-consistency of the eigenpair
    # i.e., the residual norm |r| should be small, relative to the floating
    # point error we'd expect from computing just the residuals given
    # candidate vectors.
    reltol = jnp.linalg.norm(AX, ord=2, axis=0) + theta[:k]
    reltol *= n
    # Allow some margin for a few element-wise operations.
    reltol *= 10
    res_converged = resid_norms < tol * reltol
    converged = jnp.sum(res_converged)

    new_state = i + 1, X, P, R, converged, theta[jnp.newaxis, :k]
    if debug:
      diagnostics = _generate_diagnostics(
          XPR, X, P, R, theta, converged, resid_norms / reltol)
      new_state = (new_state, diagnostics)
    return new_state

  converged = 0
  state = (0, X, P, R, converged, theta)
  if debug:
    state, diagnostics = jax.lax.scan(
        lambda state, _: body(state), state, xs=None, length=m)
  else:
    state = jax.lax.while_loop(cond, body, state)
    diagnostics = None
  i, X, _P, _R, _converged, theta = state

  if debug:
    assert diagnostics is not None
    return theta[0, :], X, i, diagnostics
  return theta[0, :], X, i

