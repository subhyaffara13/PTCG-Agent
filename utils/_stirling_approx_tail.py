
def _stirling_approx_tail(k):
  stirling_tail_vals = jnp.array(
      [
          0.0810614667953272,
          0.0413406959554092,
          0.0276779256849983,
          0.02079067210376509,
          0.0166446911898211,
          0.0138761288230707,
          0.0118967099458917,
          0.0104112652619720,
          0.00925546218271273,
          0.00833056343336287,
      ],
      dtype=k.dtype,
  )
  use_tail_values = k <= 9
  k = lax.clamp(lax._const(k, 0.0), k, lax._const(k, 9.0))
  kp1sq = (k + 1) * (k + 1)
  approx = (1.0 / 12 - (1.0 / 360 - 1.0 / 1260 / kp1sq) / kp1sq) / (k + 1)
  k = jnp.floor(k)
  return lax.select(
      use_tail_values, stirling_tail_vals[jnp.asarray(k, dtype='int32')], approx)

