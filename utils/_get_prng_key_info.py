
def _get_prng_key_info(
    specs: Sequence[api.ShapeDtypeStruct],
) -> dict[int, str]:
  """Returns a mapping from index to PRNG key impl for specs with PRNG dtypes.

  Args:
    specs: Sequence of ShapeDtypeStruct specs.

  Returns:
    A dict of integer index in `specs` to the PRNG impl for that spec. If a spec
    does not have a PRNG key dtype, it is not included in the dict.
  """
  return {
      i: spec.dtype._impl.name  # pylint: disable=protected-access
      for i, spec in enumerate(specs)
      if is_prng_key_dtype(spec.dtype)
  }

