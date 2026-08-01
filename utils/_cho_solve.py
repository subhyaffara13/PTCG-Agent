
def _cho_solve(c, b, lower, overwrite_b, check_finite):
    if check_finite:
        b1 = asarray_chkfinite(b)
        c = asarray_chkfinite(c)
    else:
        b1 = asarray(b)
        c = asarray(c)

    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("The factored matrix c is not square.")
    if c.shape[1] != b1.shape[0]:
        raise ValueError(f"incompatible dimensions ({c.shape} and {b1.shape})")

    # accommodate empty arrays
    if b1.size == 0:
        dt = cho_solve((np.eye(2, dtype=b1.dtype), True),
                        np.ones(2, dtype=c.dtype)).dtype
        return empty_like(b1, dtype=dt)

    overwrite_b = overwrite_b or _datacopied(b1, b)

    potrs, = get_lapack_funcs(('potrs',), (c, b1))
    x, info = potrs(c, b1, lower=lower, overwrite_b=overwrite_b)
    if info != 0:
        raise ValueError(f'illegal value in {-info}th argument of internal potrs')
    return x


def _cho_solve(c: ArrayLike, b: ArrayLike, lower: bool) -> Array:
  c, b = promote_dtypes_inexact(jnp.asarray(c), jnp.asarray(b))
  if b.ndim == 1:
    signature = "(n,n),(n)->(n)"
  elif c.ndim == b.ndim + 1 and c.shape[-1] == b.shape[-1]:
    # Deprecation warning added 2026-03-23
    warnings.warn(
        "jax.scipy.linalg.cho_solve: batched 1D solves with b.ndim > 1 are "
        "deprecated, and in the future will be treated as a batched 2D solve. "
        "Use cho_solve(c_and_lower, b[..., None]).squeeze(-1) to avoid this warning.",
        category=FutureWarning)
    signature = "(n,n),(n)->(n)"
  else:
    signature = "(n,n),(n,k)->(n,k)"
  b = jnp_vectorize.vectorize(
      partial(lax_linalg.triangular_solve, left_side=True, lower=lower,
              transpose_a=not lower, conjugate_a=not lower),
      signature=signature)(c, b)
  return jnp_vectorize.vectorize(
      partial(lax_linalg.triangular_solve, left_side=True, lower=lower,
              transpose_a=lower, conjugate_a=lower),
      signature=signature)(c, b)

