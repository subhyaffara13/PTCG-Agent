
def _atomic_cas_discharge_rule(in_avals, out_avals, ref, cmp, val):
  del in_avals, out_avals
  new_val = jnp.where(ref == cmp, val, ref)
  return (new_val, None, None), ref

