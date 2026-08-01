
def nonblocking_save(data: PyTreeT, directory: str | PathLike[str], *,
                     overwrite: bool = True, ts_specs: PyTreeT | None = None
                     ) -> utils.PyTreeFuture:
  """Nonblocking alias of save, return an awaitable future with a pytree stub.

  This is a simple experimental array serialization API, for anything more
  complex and for all checkpointing prefer: https://github.com/google/orbax

  Examples:
    >>> fut = nonblocking_save(data, directory)
    >>> print(fut.pytree)  # a pytree of jax.ShapeDtypeStruct's
    >>> print(fut.result())  # None, blocking until the serialization is done
  """
  # start serialization immediately
  fut = utils.PyTreeFuture(_serialization_executor.submit(
      save, data, directory, overwrite=overwrite, ts_specs=ts_specs))
  # construct a nice looking pytree representing the nodes being read
  fut.pytree = jax.tree.map(lambda x: jax.ShapeDtypeStruct(x.shape, x.dtype)
                            if _is_array_like(x) else x, data)
  return fut

