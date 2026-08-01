
def set_metadata(key: str, value: str) -> None:
  """Sets metadata for the current profiling session."""
  if hasattr(_profiler, "set_metadata"):
    return _profiler.set_metadata(key, value)


def set_metadata(
  node: tp.Any, /, *, only: filterlib.Filter = Variable, **metadata: tp.Any
) -> None:
  """Sets the metadata of all :class:`Variable` objects in the given graph node in-place.

  Example::

    >>> from flax import nnx
    >>> import jax, jax.numpy as jnp
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self):
    ...     self.param = nnx.Param(0.0)
    ...     self.variable = nnx.Variable(0.0)
    ...
    >>> node = Foo()
    ...
    >>> # set differentiable to False for all nnx.Param objects
    >>> nnx.set_metadata(node, differentiable=False, only=nnx.Param)
    ...
    >>> # check that only the nnx.Param was updated
    >>> assert node.param.get_metadata('differentiable') is False

  Args:
    node: A graph node object.
    only: A Filter to specify which :class:`Variable` objects to set metadata for.
    metadata: Key-value pairs to set as metadata on the :class:`Variable` objects.
  """
  def _set_metadata(path: PathParts, variable: V) -> None:
    del path  # unused
    if isinstance(variable, Variable):
      variable.set_metadata(**metadata)

  # inplace update of variable_state metadata
  map_state(_set_metadata, state(node, only))

