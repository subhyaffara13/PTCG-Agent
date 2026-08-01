
def _logical_to_interpret_mode_dtype(dtype):
  """Converts logical dtypes into JAX dtypes for interpret mode.

  Logical types are dtypes that exist as part of the Pallas API but
  do not have an corresponding backing type in HLO (for example,
  a Semaphore dtype).

  This function maps a logical dtype to a valid HLO dtype that can be
  used to emulate the behavior of the logical dtype (such as mapping a
  Semaphore to int).
  """
  if (hasattr(dtype, "_rules") and
      hasattr(dtype._rules, "pallas_interpret_element_aval")):
    return dtype._rules.pallas_interpret_element_aval(dtype).dtype
  return dtype

