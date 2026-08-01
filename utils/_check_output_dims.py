
def _check_output_dims(
    func: Callable,
    dim_sizes: dict[str, int],
    expected_output_core_dims: list[CoreDims],
    error_context: str = "",
) -> Callable:
  """Check that output core dimensions match the signature."""
  def wrapped(*args):
    out = func(*args)
    out_shapes = list(map(np.shape, out if isinstance(out, tuple) else [out]))

    output_core_dims = expected_output_core_dims
    if len(output_core_dims) > 1 and not isinstance(out, tuple):
      raise TypeError(
          "output must be a tuple when multiple outputs are expected, "
          "got: {!r}\n{}".format(out, error_context))
    if len(out_shapes) != len(output_core_dims):
      raise TypeError(
          'wrong number of output arguments: expected %r, got %r %s'
          % (len(output_core_dims), len(out_shapes), error_context))

    sizes = dict(dim_sizes)
    for shape, core_dims in zip(out_shapes, output_core_dims):
      _update_dim_sizes(sizes, shape, core_dims, error_context,  # pyrefly: ignore[bad-argument-type]
                        is_input=False)

    return out
  return wrapped

