
def _calculate_gather_flops(
    mode: slicing.GatherScatterMode,
    indices_size: int,
    output_size: int,
) -> int:
  """Calculates roofline unfused flops for Jax's gather primitive."""

  if mode == slicing.GatherScatterMode.FILL_OR_DROP:
    # With FILL_OR_DROP, we have 4 steps to check whether to fill (or drop):
    # 1. Check if the index is within upper bound.
    # 2. Check if the index is within lower bound.
    # 3. Call `and` on #1 and #2 to check the index is "in bounds".
    # 4. `reduce` the result to a single boolean per window.
    # Each of the steps is a single elementwise op on the indices.
    index_check_flops = indices_size * 4

    # Once we know whether to fill or drop (per window), there are 2 steps to
    # mask the output:
    # 1. Broadcast the per-window boolean to the output shape.
    # 2. Choose whether to fill (from `operand`) if in-bounds, or drop if
    #    out-of-bounds.
    # Broadcasting is free, but choosing whether to fill or drop involves an
    # elementwise op the size of the output.
    output_mask_flops = output_size
    return index_check_flops + output_mask_flops

  return 0

