
def get_ts_context(
    *,
    use_ocdbt: bool = True,
    file_io_concurrency_limit: int | None = None,
    data_copy_concurrency_limit: int | None = None,
) -> ts.Context:
  """Creates a TensorStore context object.

  For use with Orbax serialization APIs, or when directly opening a
  `TensorStore` object.

  Args:
    use_ocdbt: Whether to use OCDBT driver. Adds options specific to OCDBT if
      True.
    file_io_concurrency_limit: Optionally overrides the thread pool size for
      file I/O.
    data_copy_concurrency_limit: Optionally overrides the thread pool size for
      compressing and copying data.

  Returns:
    A TensorStore context object.
  """
  context = copy.deepcopy(
      _DEFAULT_OCDBT_TS_CONTEXT if use_ocdbt else _BASE_TS_CONTEXT
  )
  if file_io_concurrency_limit is not None:
    context.setdefault('file_io_concurrency', {})[
        'limit'
    ] = file_io_concurrency_limit
  if data_copy_concurrency_limit is not None:
    context.setdefault('data_copy_concurrency', {})[
        'limit'
    ] = data_copy_concurrency_limit
  return ts.Context(context)

