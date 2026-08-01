
def _parse_input_dimensions(args, input_core_dims):
    """
    Parse broadcast and core dimensions for vectorize with a signature.

    Arguments
    ---------
    args : Tuple[ndarray, ...]
        Tuple of input arguments to examine.
    input_core_dims : List[Tuple[str, ...]]
        List of core dimensions corresponding to each input.

    Returns
    -------
    broadcast_shape : Tuple[int, ...]
        Common shape to broadcast all non-core dimensions to.
    dim_sizes : Dict[str, int]
        Common sizes for named core dimensions.
    """
    broadcast_args = []
    dim_sizes = {}
    for arg, core_dims in zip(args, input_core_dims):
        _update_dim_sizes(dim_sizes, arg, core_dims)
        ndim = arg.ndim - len(core_dims)
        dummy_array = np.lib.stride_tricks.as_strided(0, arg.shape[:ndim])
        broadcast_args.append(dummy_array)
    broadcast_shape = np.lib._stride_tricks_impl._broadcast_shape(
        *broadcast_args
    )
    return broadcast_shape, dim_sizes


def _parse_input_dimensions(
    args: tuple[NDArray, ...],
    input_core_dims: list[CoreDims],
    error_context: str = "",
) -> tuple[tuple[int, ...], dict[str, int]]:
  """Parse broadcast and core dimensions for vectorize with a signature.

  Args:
    args: tuple of input arguments to examine.
    input_core_dims: list of core dimensions corresponding to each input.
    error_context: string context for error messages.

  Returns:
    broadcast_shape: common shape to broadcast all non-core dimensions to.
    dim_sizes: common sizes for named core dimensions.
  """
  if len(args) != len(input_core_dims):
    raise TypeError(
        'wrong number of positional arguments: expected %r, got %r %s'
        % (len(input_core_dims), len(args), error_context))
  shapes: list[tuple[int, ...]] = []
  dim_sizes: dict[str, int] = {}
  for arg, core_dims in zip(args, input_core_dims):
    _update_dim_sizes(dim_sizes, arg.shape, core_dims, error_context,
                      is_input=True)
    ndim = arg.ndim - len(core_dims)
    shapes.append(arg.shape[:ndim])
  broadcast_shape = lax.broadcast_shapes(*shapes)
  # TODO(mattjj): this code needs updating for dynamic shapes (hence ignore)
  return broadcast_shape, dim_sizes

