
def _convert_inp_type_to_physical(
    inp_type: Sequence[api.ShapeDtypeStruct],
    prng_info: dict[int, str],
) -> tuple[api.ShapeDtypeStruct, ...]:
  """Converts PRNG key types to physical types, leaving others unchanged."""
  if not prng_info:
    return tuple(inp_type)
  inp_type = list(inp_type)
  for i in prng_info:
    inp_type[i] = _prng_key_type_to_physical_spec(inp_type[i])
  return tuple(inp_type)

