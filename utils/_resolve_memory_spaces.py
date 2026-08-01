
def _resolve_memory_spaces(
    in_avals: Sequence[jax_core.AbstractValue],
    out_avals: Sequence[jax_core.AbstractValue],
    *,
    input_output_aliases: tuple[tuple[int, int], ...],
    kernel_type: tpu_core.CoreType | None,
) -> tuple[
    tuple[tpu_custom_call.MemorySpace | None, ...] | None,
    tuple[tpu_custom_call.MemorySpace | None, ...] | None,
]:
  output_memory_spaces = _get_memory_spaces_from_avals(
      out_avals, kernel_type=kernel_type
  )
  input_memory_spaces = None
  if any(isinstance(aval, jax_core.ShapedArray)
         and not isinstance(aval.memory_space, jax_core.MemorySpace)
         for aval in in_avals):
    input_memory_spaces = _get_memory_spaces_from_avals(
        in_avals, kernel_type=kernel_type
    )
    # ShapedArrayWithMemorySpace wasn't allowed to escape the Pallas kernel, so
    # it was stripped from the original out_avals. We need to resolve this for
    # outputs aliased to inputs with pltpu.with_memory_space_constraint.
    if input_memory_spaces is not None:
      output_memory_spaces_list: list[tpu_custom_call.MemorySpace | None]
      if output_memory_spaces is None:
        output_memory_spaces_list = [None] * len(out_avals)
      else:
        output_memory_spaces_list = list(output_memory_spaces)
      modified = False
      for in_idx, out_idx in input_output_aliases:
        if (ms := input_memory_spaces[in_idx]) is not None:
          if (out_ms := output_memory_spaces_list[out_idx]) not in (None, ms):
            raise ValueError(
                f"In/out memory space conflict for alias {in_idx}->{out_idx}:"
                f" {ms} != {out_ms}"
            )
          output_memory_spaces_list[out_idx] = ms
          modified = True
      if modified:
        output_memory_spaces = tuple(output_memory_spaces_list)
  if output_memory_spaces is not None:
    input_memory_spaces_list: list[tpu_custom_call.MemorySpace | None]
    if input_memory_spaces is None:
      input_memory_spaces_list = [None] * len(in_avals)
    else:
      input_memory_spaces_list = list(input_memory_spaces)
    modified = False
    for in_idx, out_idx in input_output_aliases:
      if (ms := output_memory_spaces[out_idx]) is not None:
        if (in_ms := input_memory_spaces_list[in_idx]) not in (None, ms):
          raise ValueError(
              f"In/out memory space conflict for alias {in_idx}->{out_idx}:"
              f"{in_ms} != {ms}"
          )
        input_memory_spaces_list[in_idx] = ms
        modified = True
    if modified:
      input_memory_spaces = tuple(input_memory_spaces_list)
  if input_memory_spaces is not None:
    input_memory_spaces = tuple(
        i
        if i
        in {
            tpu_custom_call.MemorySpace.HBM,
            tpu_custom_call.MemorySpace.VMEM,
            tpu_custom_call.MemorySpace.SMEM,
        }
        else None
        for i in input_memory_spaces
    )
  return input_memory_spaces, output_memory_spaces

