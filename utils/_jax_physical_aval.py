
def _jax_physical_aval(aval: core.ShapedArray) -> core.ShapedArray:
  """Converts JAX avals from logical to physical, if relevant.

  JAX might have avals whose logical vs physical shape/dtype may
  differ, and only the physical view is expected to possibly
  relate to TF. TF impl rules should operate on the physical form.

  A JAX logical aval might even correspond, in principle, to several
  physical avals, but we don't support those here. Instead we assert
  there is only one and return it.
  """
  physical_aval = core.physical_aval(aval)
  assert (len(physical_aval.shape) >= len(aval.shape) and
          physical_aval.shape[:len(aval.shape)] == aval.shape), (physical_aval, aval)
  return physical_aval

