
def _update_dim_sizes(dim_sizes, arg, core_dims):
    """
    Incrementally check and update core dimension sizes for a single argument.

    Arguments
    ---------
    dim_sizes : Dict[str, int]
        Sizes of existing core dimensions. Will be updated in-place.
    arg : ndarray
        Argument to examine.
    core_dims : Tuple[str, ...]
        Core dimensions for this argument.
    """
    if not core_dims:
        return

    num_core_dims = len(core_dims)
    if arg.ndim < num_core_dims:
        raise ValueError(
            f'{arg.ndim}-dimensional argument does not have enough '
            f'dimensions for all core dimensions {core_dims!r}')

    core_shape = arg.shape[-num_core_dims:]
    for dim, size in zip(core_dims, core_shape):
        if dim in dim_sizes:
            if size != dim_sizes[dim]:
                raise ValueError(
                    f'inconsistent size for core dimension {dim!r}: {size!r} vs '
                    f'{dim_sizes[dim]!r}'
                )
        else:
            dim_sizes[dim] = size


def _update_dim_sizes(
    dim_sizes: dict[str, int],
    shape: tuple[int, ...],
    core_dims: CoreDims,
    error_context: str = "",
    *,
    is_input: bool):
  """Incrementally check and update core dimension sizes for a single argument.

  Args:
    dim_sizes: sizes of existing core dimensions. Will be updated in-place.
    shape: shape of this argument.
    core_dims: core dimensions for this argument.
    error_context: string context for error messages.
    is_input: are we parsing input or output arguments?
  """
  num_core_dims = len(core_dims)
  if is_input:
    if len(shape) < num_core_dims:
      raise ValueError(
          'input with shape %r does not have enough dimensions for all core '
          'dimensions %r %s' % (shape, core_dims, error_context))
  else:
    if len(shape) != num_core_dims:
      raise ValueError(
          'output shape %r does not match core dimensions %r %s'
          % (shape, core_dims, error_context))

  core_shape = shape[-num_core_dims:] if core_dims else ()
  for dim, size in zip(core_dims, core_shape):
    if dim not in dim_sizes:
      dim_sizes[dim] = size
    elif size != dim_sizes[dim]:
      raise ValueError(
          'inconsistent size for core dimension %r: %r vs %r %s'
          % (dim, size, dim_sizes[dim], error_context))

