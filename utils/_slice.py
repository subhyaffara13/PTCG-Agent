
def _slice(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    axes: list | torch.Tensor | torch._C.Value,
    starts: list | torch.Tensor | torch._C.Value,
    ends: list | torch.Tensor | torch._C.Value,
    steps: list | torch.Tensor | torch._C.Value | None = None,
):
    def is_none_value(value):
        if value is None:
            return True
        return (
            isinstance(value, torch._C.Value)
            and value.node().kind() == "prim::Constant"
            and isinstance(value.type(), _C.NoneType)
        )

    def to_slice_input(list_or_value, default_value=None):
        # Convert input param into a 1D torch.Value.
        if is_none_value(list_or_value) and default_value is not None:
            list_or_value = [default_value]

        if isinstance(list_or_value, torch.Tensor):
            return g.op("Constant", value_t=list_or_value.clone().detach())
        elif isinstance(list_or_value, list):
            return g.op("Constant", value_t=torch.tensor(list_or_value))

        rank = symbolic_helper._get_tensor_rank(list_or_value)
        if rank == 0:
            return symbolic_helper._unsqueeze_helper(g, list_or_value, [0])
        if rank == 1:
            return list_or_value
        raise errors.SymbolicValueError(
            f"Rank must be 0 or 1, not {rank}", list_or_value
        )

    def get_const_value(list_or_value):
        if isinstance(list_or_value, (list, torch.Tensor)):
            if len(list_or_value) == 1:
                return list_or_value[0]
            return None
        return symbolic_helper._maybe_get_const(list_or_value, "i")

    # Check if slice is a no-op
    if (
        get_const_value(starts) == 0
        and get_const_value(ends) == _constants.INT64_MAX
        and (steps is None or get_const_value(steps) == 1)
    ):
        return input

    axes = to_slice_input(axes)
    starts = to_slice_input(starts, default_value=0)
    ends = to_slice_input(ends, default_value=_constants.INT64_MAX)
    if steps is None:
        return g.op("Slice", input, starts, ends, axes)
    steps = to_slice_input(steps, default_value=1)
    return g.op("Slice", input, starts, ends, axes, steps)


def _slice(g: jit_utils.GraphContext, input, axes, starts, ends):
    if len(starts) != len(ends):
        raise AssertionError(f"len(starts)={len(starts)} != len(ends)={len(ends)}")
    if len(starts) == 1 and starts[0] == 0 and ends[0] == _constants.INT64_MAX:
        return input
    return g.op("Slice", input, axes_i=axes, starts_i=starts, ends_i=ends)


def _slice(operand, start_indices, dynamic_slice_sizes, static_slice_sizes,
           fill_value=0):
  """Similar to lax.dynamic_slice, but handles arrays with dynamic sizes.

  Returns fill_value instead of clamping start_indices for those elements that
  would overflow the side of the array.

  Args:
    operand: the array to slice
    start_indices: the offset of the start of the slice
    dynamic_slice_sizes: the true (unpadded) size of the slice
    static_slice_sizes: the padded size of the slice, which must be known at
      compile time. The static size must be larger than the dynamic size.
    fill_value: value with which to replace masked-out elements.
  Returns:
    An array with static shape `static_slice_sizes`, padded from its true
    (dynamic) size `dynamic_slice_sizes`.
  """
  # We must pad the input array so the dynamic_slice is guaranteed to fall
  # entirely in bounds.
  padded = lax.pad(operand,
                   jnp.array(0, operand.dtype),
                   [(0, d, 0) for d in static_slice_sizes])
  out = lax.dynamic_slice(padded, tuple(jnp.array(i, np.int32) for i in start_indices),
                          static_slice_sizes)
  return _mask(out, dynamic_slice_sizes, fill_value)

