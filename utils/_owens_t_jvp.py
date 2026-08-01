
def _owens_t_jvp(primals, tangents):
  (h, a) = primals
  (dh, da) = tangents
  result = _owens_t_impl(h, a)
  root_2 = _lax_const(h, np.sqrt(2))
  # ∂T/∂h = -exp(-h²/2) · erf(ah/√2) / (2√(2π))
  dout_dh = (-lax.exp(-0.5 * lax.square(h)) * lax.erf(a * h / root_2)
             / (2. * _lax_const(h, np.sqrt(2. * np.pi))))
  # ∂T/∂a = exp(-½(a²+1)h²) / (2π(a²+1))
  dout_da = (lax.exp(-0.5 * (lax.square(a) + 1.) * lax.square(h))
             / (2. * np.pi * (lax.square(a) + 1.)))
  return result, (dout_dh * dh + dout_da * da).astype(result.dtype)

