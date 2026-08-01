
def pop(g: jit_utils.GraphContext, tensor_list, dim):
    return g.op("SequenceErase", tensor_list, dim)


def pop(
  x: FrozenDict | dict[str, Any], key: str
) -> tuple[FrozenDict | dict[str, Any], Any]:
  """Create a new dict where one entry is removed. This is a utility
  function that can act on either a FrozenDict or regular dict and
  mimics the behavior of ``FrozenDict.pop``.

  Example::

    >>> from flax.core import FrozenDict, pop
    >>> variables = FrozenDict({'params': {...}, 'batch_stats': {...}})
    >>> new_variables, params = pop(variables, 'params')

  Args:
    x: the dictionary to remove the entry from
    key: the key to remove from the dict
  Returns:
    A pair with the new dict and the removed value.
  """

  if isinstance(x, FrozenDict):
    return x.pop(key)
  elif isinstance(x, dict):
    new_dict = jax.tree_util.tree_map(
        lambda x: x, x
    )  # make a deep copy of dict x
    value = new_dict.pop(key)
    return new_dict, value
  raise TypeError(f'Expected FrozenDict or dict, got {type(x)}')


def pop(
  node,
  filter: filterlib.Filter,
  /,
) -> State: ...


def pop(
  node,
  filter: filterlib.Filter,
  filter2: filterlib.Filter,
  /,
  *filters: filterlib.Filter,
) -> tuple[State, ...]: ...


def pop(
  node, *filters: filterlib.Filter
) -> tp.Union[State, tuple[State, ...]]:
  """Pop one or more :class:`Variable` types from the graph node.

  Example usage::

    >>> from flax import nnx
    >>> import jax.numpy as jnp

    >>> class Model(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.linear1 = nnx.Linear(2, 3, rngs=rngs)
    ...     self.linear2 = nnx.Linear(3, 4, rngs=rngs)
    ...   def __call__(self, x):
    ...     x = self.linear1(x)
    ...     self.i = nnx.Intermediate(x)
    ...     x = self.linear2(x)
    ...     return x

    >>> x = jnp.ones((1, 2))
    >>> model = Model(rngs=nnx.Rngs(0))
    >>> assert not hasattr(model, 'i')
    >>> y = model(x)
    >>> assert hasattr(model, 'i')

    >>> intermediates = nnx.pop(model, nnx.Intermediate)
    >>> assert intermediates['i'].shape == (1, 3)
    >>> assert not hasattr(model, 'i')

  Args:
    node: A graph node object.
    *filters: One or more :class:`Variable` objects to filter by.
  Returns:
    The popped :class:`State` containing the :class:`Variable`
    objects that were filtered for.
  """
  if len(filters) == 0:
    raise ValueError('Expected at least one filter')

  id_to_index: dict[int, Index] = {}
  path_parts: PathParts = ()
  predicates = tuple(filterlib.to_predicate(filter) for filter in filters)
  flat_states: tuple[dict[PathParts, LeafType], ...] = tuple(
    {} for _ in predicates
  )
  _graph_pop(
    node=node,
    id_to_index=id_to_index,
    path_parts=path_parts,
    flat_states=flat_states,
    predicates=predicates,
  )
  states = tuple(
    statelib.from_flat_state(flat_state) for flat_state in flat_states
  )

  if len(states) == 1:
    return states[0]
  else:
    return states

