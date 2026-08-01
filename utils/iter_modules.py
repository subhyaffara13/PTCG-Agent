
def iter_modules(
  module: Module, /, *, graph: bool | None = None,
) -> tp.Iterator[tuple[PathParts, Module]]:
  """Recursively iterates over all nested :class:`Module`'s of the given Module, including
  the argument.

  Specifically, this function creates a generator that yields the path and the Module instance, where
  the path is a tuple of strings or integers representing the path to the Module from the
  root Module.

  Example::

    >>> from flax import nnx
    ...
    >>> class SubModule(nnx.Module):
    ...   def __init__(self, din, dout, rngs):
    ...     self.linear1 = nnx.Linear(din, dout, rngs=rngs)
    ...     self.linear2 = nnx.Linear(din, dout, rngs=rngs)
    ...
    >>> class Block(nnx.Module):
    ...   def __init__(self, din, dout, *, rngs: nnx.Rngs):
    ...     self.linear = nnx.Linear(din, dout, rngs=rngs)
    ...     self.submodule = SubModule(din, dout, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5)
    ...     self.batch_norm = nnx.BatchNorm(10, rngs=rngs)
    ...
    >>> model = Block(2, 5, rngs=nnx.Rngs(0))
    >>> for path, module in nnx.iter_modules(model):
    ...   print(path, type(module).__name__)
    ...
    ('batch_norm',) BatchNorm
    ('dropout',) Dropout
    ('linear',) Linear
    ('submodule', 'linear1') Linear
    ('submodule', 'linear2') Linear
    ('submodule',) SubModule
    () Block

  Args:
    module: A :class:`Module` object.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  """
  for path, value in graphlib.iter_graph(module, graph=graph):
    if isinstance(value, Module):
      yield path, value

