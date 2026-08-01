
def _solve_triangular(a1, b1, trans=0, lower=False, unit_diagonal=False,
                      overwrite_b=False):

    trans = {'N': 0, 'T': 1, 'C': 2}.get(trans, trans)
    trtrs, = get_lapack_funcs(('trtrs',), (a1, b1))
    if a1.flags.f_contiguous or trans == 2:
        x, info = trtrs(a1, b1, overwrite_b=overwrite_b, lower=lower,
                        trans=trans, unitdiag=unit_diagonal)
    else:
        # transposed system is solved since trtrs expects Fortran ordering
        x, info = trtrs(a1.T, b1, overwrite_b=overwrite_b, lower=not lower,
                        trans=not trans, unitdiag=unit_diagonal)

    if info == 0:
        return x, info
    if info > 0:
        raise LinAlgError(f"singular matrix: resolution failed at diagonal {info-1}")
    raise ValueError(f'illegal value in {-info}-th argument of internal trtrs')


def _solve_triangular(a: ArrayLike, b: ArrayLike, trans: int | str,
                      lower: bool, unit_diagonal: bool) -> Array:
  if trans == 0 or trans == "N":
    transpose_a, conjugate_a = False, False
  elif trans == 1 or trans == "T":
    transpose_a, conjugate_a = True, False
  elif trans == 2 or trans == "C":
    transpose_a, conjugate_a = True, True
  else:
    raise ValueError(f"Invalid 'trans' value {trans}")

  a, b = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))

  if b.ndim == 1:
    signature = "(n,n),(n)->(n)"
  elif a.ndim == b.ndim + 1 and a.shape[-1] == b.shape[-1]:
    # Deprecation warning added 2026-03-23
    warnings.warn(
        "jax.scipy.linalg.solve_triangular: batched 1D solves with b.ndim > 1 "
        "are deprecated, and in the future will be treated as a batched 2D solve. "
        "Use solve_triangular(a, b[..., None]).squeeze(-1) to avoid this warning.",
        category=FutureWarning)
    signature = "(n,n),(n)->(n)"
  else:
    signature = "(n,n),(n,k)->(n,k)"

  return jnp_vectorize.vectorize(
      partial(lax_linalg.triangular_solve, left_side=True, lower=lower,
              transpose_a=transpose_a, conjugate_a=conjugate_a,
              unit_diagonal=unit_diagonal),
      signature=signature)(a, b)

