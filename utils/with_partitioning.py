
def with_partitioning(
    fn: Callable[..., Any],
    names: LogicalNames,
    mesh: jax.sharding.Mesh | None = None,
) -> Callable[..., Partitioned[Any]]:
  """Wraps a function's return value with Partitioned.

  Example::

    >>> import flax.linen as nn
    >>> kernel_init = nn.with_partitioning(
    ...     nn.initializers.lecun_normal(), (None, "data"))
    >>> partitioned_dense = nn.Dense(features=3, kernel_init=kernel_init)

  Args:
    fn: The function to be wrapped. Typically this is an initializer.
    names: The logical axis passed to ``Partitioned``.
    mesh: The mesh to use for the partitioning. If None, the global mesh
      resource is used if available.

  Returns:
    A function wrapping ``fn`` that will return an instance of ``Partitioned``.
  """

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    return Partitioned(fn(*args, **kwargs), names, mesh=mesh)

  return wrapper


def with_partitioning(
  initializer: F,
  sharding: Sharding,
  mesh: tp.Optional[jax.sharding.Mesh] = None,
  **metadata: tp.Any,
) -> F:
  """A wrapper over any initializer to add sharding annotation data to a `Variable`."""
  return variablelib.with_metadata(
    initializer,
    out_sharding=sharding,
    mesh=mesh,
    **metadata,
  )


def with_partitioning(
    fn: tp.Callable[..., tp.Any],
    names: LogicalNames,
    mesh: jax.sharding.Mesh | None = None,
) -> tp.Callable[..., meta.Partitioned[tp.Any]]:
  """Same interface as Linen, but calls NNX `with_partitioning` within."""
  return spmd.with_partitioning(fn, names, mesh,
                                linen_meta_type=meta.Partitioned)
