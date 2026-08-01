
def clone(x, *, memory_format=None):
    # TODO(jansel): memory format
    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=x.make_loader(),
        ranges=list(x.get_size()),
    )


def clone(
    a: TensorLikeType, *, memory_format: torch.memory_format = torch.preserve_format
) -> TensorLikeType:
    result = prims.clone(a, memory_format=memory_format)
    return result


def clone(g: jit_utils.GraphContext, input, unused_memory_format):
    return input


def clone(key):
  """Clone a key for reuse

  Outside the context of key reuse checking (see :mod:`jax.experimental.key_reuse`)
  this function operates as an identity.

  Examples:

    >>> import jax
    >>> key = jax.random.key(0)
    >>> data = jax.random.uniform(key)
    >>> cloned_key = jax.random.clone(key)
    >>> same_data = jax.random.uniform(cloned_key)
    >>> assert data == same_data
  """
  return random_clone_p.bind(key)


def clone(node: Node, variables: bool = True, *, graph: bool | None = None) -> Node:
  """Create a deep copy of the given graph node.

  Example usage::

    >>> from flax import nnx

    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> cloned_model = nnx.clone(model)
    >>> model.bias[...] += 1
    >>> assert (model.bias[...] != cloned_model.bias[...]).all()

  Args:
    node: A graph node object.
    variables: If ``True`` (default) copies of the :class:`Variable` objects are created,
      otherwise the Variables are shared between the original and cloned node.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    A deep copy of the :class:`Module` object.
  """
  graphdef, state = split(node, graph=graph)
  return merge(graphdef, state, copy=variables)

