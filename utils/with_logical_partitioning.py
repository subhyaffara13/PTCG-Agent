
def with_logical_partitioning(
  fn: Callable[..., Any],
  names: LogicalNames,
  mesh: jax.sharding.Mesh | None = None,
  rules: LogicalRules | None = None,
) -> Callable[..., LogicallyPartitioned]:
  """Wraps a function's return value with LogicallyPartitioned.

  Example::

    >>> import flax.linen as nn
    >>> kernel_init = nn.with_logical_partitioning(
    ...     nn.initializers.lecun_normal(), (None, "data"))
    >>> partitioned_dense = nn.Dense(features=3, kernel_init=kernel_init)

  Args:
    fn: The function to be wrapped. Typically this is an initializer.
    names: The logical axis passed to ``LogicallyPartitioned``.
    mesh: The mesh to use for the partitioning. If None, the global mesh
      resource is used if available.
    rules: Optional logical to mesh rules use. If None, the global rules
      are used if available.
  Returns:
    A function wrapping ``fn`` that will return an instance of
    ``LogicallyPartitioned``.
  """

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    return LogicallyPartitioned(
      fn(*args, **kwargs), names, mesh=mesh, rules=rules
    )  # pytype: disable=wrong-keyword-args

  return wrapper

