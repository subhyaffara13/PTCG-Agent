
def tridiagonal_solve(dl: Array, d: Array, du: Array, b: Array, *,
                      perturb_singular: bool = False) -> Array:
  r"""Computes the solution of a tridiagonal linear system.

  This function computes the solution of a tridiagonal linear system:

  .. math::
    A \, X = B

  Args:

    dl: A batch of vectors with shape ``[..., m]``.
      The lower diagonal of A: ``dl[i] := A[i, i-1]`` for i in ``[0,m)``.
      Note that ``dl[0] = 0``.
    d: A batch of vectors with shape ``[..., m]``.
      The middle diagonal of A: ``d[i]  := A[i, i]`` for i in ``[0,m)``.
    du: A batch of vectors with shape ``[..., m]``.
      The upper diagonal of A: ``du[i] := A[i, i+1]`` for i in ``[0,m)``.
      Note that ``dl[m - 1] = 0``.
    b: Right hand side matrix.
    perturb_singular: Whether to perturb singular matrices to return a finite
      result. ``False`` by default. If ``True``, solutions to systems involving
      a singular matrix will be computed by perturbing near-zero pivots in
      the partially pivoted LU decomposition. Specifically, tiny pivots are
      perturbed by an amount of order ``eps * max_{ij} |U(i,j)|`` to avoid
      overflow. Here ``U`` is the upper triangular part of the LU decomposition,
      and ``eps`` is the machine precision. This is useful for solving
      numerically singular systems when computing eigenvectors by inverse
      iteration. Only implemented on CPU and GPU at the moment.

  Returns:
    Solution ``X`` of tridiagonal system.
  """
  if perturb_singular and jaxlib_version < (0, 10):
    raise RuntimeError("perturb_singular=True requires jaxlib >= 0.10.0.")
  dl, d, du, b = core.auto_insert_reshard(dl, d, du, b)
  return tridiagonal_solve_p.bind(
    dl, d, du, b, perturb_singular=perturb_singular)

