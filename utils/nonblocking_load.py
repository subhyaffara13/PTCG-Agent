
def nonblocking_load(directory: str | PathLike[str], shardings: PyTreeT, *,
                     mask: PyTreeT | None = None,
                     ts_specs: PyTreeT | None = None) -> utils.PyTreeFuture:
  """Nonblocking alias of load, return an awaitable future with a pytree stub.

  This is a simple experimental array serialization API, for anything more
  complex and for all checkpointing prefer: https://github.com/google/orbax

  Examples:
    >>> fut = nonblocking_load(directory)
    >>> print(fut.pytree)  # a pytree of jax.ShapeDtypeStruct
    >>> print(fut.result())  # the fully populated pytree
  """
  # TODO(rdyro): the awaitable future output is a workaround
  # it should return the fully populated pytree instead of just
  # jax.ShapeDtypeStruct for arrays by constructing them asynchronously
  fut = utils.PyTreeFuture(_serialization_executor.submit(
      load, directory, shardings, mask=mask, ts_specs=ts_specs))
  fut.pytree = load_pytreedef(directory)
  return fut

