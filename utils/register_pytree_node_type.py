
def register_pytree_node_type(
  type: type,
  flatten: tp.Callable[[Node], tuple[tp.Sequence[tuple[Key, Leaf]], AuxData]],
  unflatten: tp.Callable[[tp.Sequence[tuple[Key, Leaf]], AuxData], Node],
  *,
  set_key: tp.Callable[[Node, Key, Leaf], None] | None = None,
  pop_key: tp.Callable[[Node, Key], Leaf] | None = None,
):
  if type in PYTREE_REGISTRY:
    raise ValueError(f'Node type {type} is already registered.')

  PYTREE_REGISTRY[type] = PytreeNodeImpl(
    type=type,
    flatten=flatten,
    unflatten=unflatten,
    set_key=set_key,
    pop_key=pop_key,
  )

