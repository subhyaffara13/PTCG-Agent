
def _dawsn_impl(x: Array) -> Array:
  # Rational approximations from Cody, Paciorek, Thacher (1970).
  # All approximations work on |x|; odd symmetry restores the sign.
  sign = jnp.sign(x)
  # sign(0) == 0, but dawsn(0) == 0 so the product is correct.
  ax = lax.abs(x)

  AN = np.array(_DAWSN_AN, dtype=x.dtype)
  AD = np.array(_DAWSN_AD, dtype=x.dtype)
  BN = np.array(_DAWSN_BN, dtype=x.dtype)
  BD = np.array(_DAWSN_BD, dtype=x.dtype)
  CN = np.array(_DAWSN_CN, dtype=x.dtype)
  CD = np.array(_DAWSN_CD, dtype=x.dtype)

  ax2 = lax.square(ax)
  t = _lax_const(x, 1.) / ax2

  # Compute each region using safe dummy inputs to avoid NaN in unused branches.
  # (Without safe inputs, polyval at extreme ax values overflows to inf, and
  # inf/inf = NaN which lax.select does not suppress on all backends.)
  # Region 1
  safe_ax_r1 = lax.select(ax < _lax_const(x, 3.25), ax, lax.full_like(ax, 1.))
  safe_ax2_r1 = lax.square(safe_ax_r1)
  val_r1 = safe_ax_r1 * jnp.polyval(AN, safe_ax2_r1) / jnp.polyval(AD, safe_ax2_r1)

  # Region 2
  safe_t_r2 = lax.select(
      (ax >= _lax_const(x, 3.25)) & (ax < _lax_const(x, 6.25)),
      t, lax.full_like(t, 1.))
  safe_ax_r2 = lax.select(
      (ax >= _lax_const(x, 3.25)) & (ax < _lax_const(x, 6.25)),
      ax, lax.full_like(ax, 1.))
  val_r2 = (_lax_const(x, 0.5) / safe_ax_r2) * (
      _lax_const(x, 1.)
      + safe_t_r2 * jnp.polyval(BN, safe_t_r2) / jnp.polyval(BD, safe_t_r2))

  # Region 3
  safe_t_r3 = lax.select(ax >= _lax_const(x, 6.25), t, lax.full_like(t, 1.))
  safe_ax_r3 = lax.select(ax >= _lax_const(x, 6.25), ax, lax.full_like(ax, 1.))
  val_r3 = (_lax_const(x, 0.5) / safe_ax_r3) * (
      _lax_const(x, 1.)
      + safe_t_r3 * jnp.polyval(CN, safe_t_r3) / jnp.polyval(CD, safe_t_r3))

  result = lax.select(ax < _lax_const(x, 3.25), val_r1,
                      lax.select(ax < _lax_const(x, 6.25), val_r2, val_r3))
  return sign * result

