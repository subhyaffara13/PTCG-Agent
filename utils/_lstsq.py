
def _lstsq(a, b, xp=None, rcond=None):
    a, b = xp_promote(a, b, force_floating=True, xp=xp)

    if rcond is None:
        rcond = xp.finfo(a.dtype).eps

    if is_numpy(xp):
        from scipy.linalg import lstsq as s_lstsq
        return s_lstsq(a, b, cond=rcond)
    elif lstsq_func := getattr(xp.linalg, "lstsq", None):
        # cupy, torch, jax.numpy all have xp.linalg.lstsq
        return lstsq_func(a, b, rcond=rcond)
    else:
        # unknown array library: LSQ solve via pseudoinverse
        u, s, vt = xp.linalg.svd(a, full_matrices=False)

        sing_val_mask = s > rcond
        s = xpx.apply_where(sing_val_mask, (s,), lambda x: 1. / x, fill_value=0.)

        sigma = xp.eye(s.shape[0]) * s    # == np.diag(s)
        x = vt.T @ sigma @ u.T @ b

        rank = xp.count_nonzero(sing_val_mask)

        # XXX actually compute residuals, when there's a use case
        residuals = xp.asarray([])
        return x, residuals, rank, s


def _lstsq(a: ArrayLike, b: ArrayLike, rcond: Array | float | None, *,
           numpy_resid: bool = False) -> tuple[Array, Array, Array, Array]:
  # TODO: add lstsq to lax_linalg and implement this function via those wrappers.
  # TODO: add custom jvp rule for more robust lstsq differentiation
  a, b = promote_dtypes_inexact(a, b)
  if a.shape[0] != b.shape[0]:
    raise ValueError("Leading dimensions of input arrays must match")
  b_orig_ndim = b.ndim
  if b_orig_ndim == 1:
    b = b[:, None]
  if a.ndim != 2:
    raise TypeError(
      f"{a.ndim}-dimensional array given. Array must be two-dimensional")
  if b.ndim != 2:
    raise TypeError(
      f"{b.ndim}-dimensional array given. Array must be one or two-dimensional")
  m, n = a.shape
  dtype = a.dtype
  if a.size == 0:
    s = array_creation.empty(0, dtype=a.dtype)
    rank = jnp.array(0, dtype=int)
    x = array_creation.zeros((n, *b.shape[1:]), dtype=a.dtype)
  else:
    if rcond is None:
      rcond = float(jnp.finfo(dtype).eps) * max(n, m)
    else:
      rcond = jnp.where(rcond < 0, jnp.finfo(dtype).eps, rcond)
    u, s, vt = svd(a, full_matrices=False)
    mask = (s > 0) & (s >= jnp.array(rcond, dtype=s.dtype) * s[0])
    rank = mask.sum()
    safe_s = jnp.where(mask, s, 1).astype(a.dtype)
    s_inv = jnp.where(mask, 1 / safe_s, 0)[:, np.newaxis]
    uTb = tensor_contractions.matmul(u.conj().T, b, precision=lax.Precision.HIGHEST)
    x = tensor_contractions.matmul(vt.conj().T, s_inv * uTb, precision=lax.Precision.HIGHEST)
  # Numpy returns empty residuals in some cases. To allow compilation, we
  # default to returning full residuals in all cases.
  if numpy_resid and (rank < n or m <= n):
    resid = jnp.asarray([])
  else:
    b_estimate = tensor_contractions.matmul(a, x, precision=lax.Precision.HIGHEST)
    resid = norm(b - b_estimate, axis=0) ** 2
  if b_orig_ndim == 1:
    x = x.ravel()
  return x, resid, rank, s


def _lstsq(a, b):
  # faster than jsp_linalg.lstsq
  a2 = _dot(a.T.conj(), a)
  b2 = _dot(a.T.conj(), b)
  return jsp_linalg.solve(a2, b2, assume_a='pos')

