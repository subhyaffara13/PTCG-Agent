
def _broadcast_input_output_aliases(
    args: Sequence[jax_typing.Array],
    dims: Sequence[int | batching.NotMapped],
    *,
    input_output_aliases: tuple[tuple[int, int], ...],
    axis_size: int,
) -> tuple[tuple[jax_typing.Array, ...], tuple[int | batching.NotMapped, ...]]:
  """Broadcast input/output operands.

  When we have input/output aliasing, since the output will be mapped, we need
  to make sure to broadcast the input across that dimension if it is not
  mapped. If the input is mapped, but on a different axis, we transpose the input
  to match the output.
  """

  args_ = list(args)
  dims_ = list(dims)
  for input_index, _ in input_output_aliases:
    dim = dims_[input_index]
    dims_[input_index] = 0
    if dim is None:
      args_[input_index] = batching.broadcast(
          args_[input_index], axis_size, 0, None)
    elif dim != 0:
      # TODO(cjfj): Change output batching axis instead?

      args_[input_index] = jnp.moveaxis(args[input_index], dim, 0)

  return tuple(args_), tuple(dims_)

