
def _gmres_solve(A, b, x0, atol, ptol, restart, maxiter, M, gmres_func):
  """
  The main function call wrapped by custom_linear_solve. Repeatedly calls GMRES
  to find the projected solution within the order-``restart``
  Krylov space K(A, x0, restart), using the result of the previous projection
  in place of x0 each time. Parameters are the same as in ``gmres`` except:

  atol: Tolerance for norm(A(x) - b), used between restarts.
  ptol: Tolerance for norm(M(A(x) - b)), used within a restart.
  gmres_func: A function performing a single GMRES restart.

  Returns: The solution.
  """
  residual = M(_sub(b, A(x0)))
  unit_residual, residual_norm = _safe_normalize(residual)

  def cond_fun(value):
    _, k, _, residual_norm = value
    return jnp.logical_and(k < maxiter, residual_norm > atol)

  def body_fun(value):
    x, k, unit_residual, residual_norm = value
    x, unit_residual, residual_norm = gmres_func(
        A, b, x, unit_residual, residual_norm, ptol, restart, M)
    return x, k + 1, unit_residual, residual_norm

  initialization = (x0, 0, unit_residual, residual_norm)
  x_final, k, _, err = lax.while_loop(cond_fun, body_fun, initialization)
  _ = k  # Until we can pass this out
  _ = err
  return x_final  # , info

