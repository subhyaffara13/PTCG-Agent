
def _initialize_output_vals(
    block_mappings_output: Iterable[BlockMapping],
    input_args, input_output_aliases) -> Sequence[jax_typing.Array]:
  oi_map = {v: k for k, v in input_output_aliases}
  output_vals = []
  for i, bm in enumerate(block_mappings_output):
    if i in oi_map:
      output_vals.append(input_args[oi_map[i]])
    else:
      output_vals.append(primitives.uninitialized_value(
          bm.array_aval.shape,
          bm.array_aval.dtype))
  return output_vals

