
def register_graph_node_type(
  type: type,
  flatten: tp.Callable[[Node], tuple[tp.Sequence[tuple[Key, Leaf]], AuxData]],
  set_key: tp.Callable[[Node, Key, Leaf], None],
  pop_key: tp.Callable[[Node, Key], Leaf],
  create_empty: tp.Callable[[AuxData], Node],
  clear: tp.Callable[[Node], None],
  init: tp.Callable[[Node, tp.Iterable[tuple[Key, Leaf]]], None],
):
  if type in GRAPH_REGISTRY:
    raise ValueError(f'Node type {type} is already registered.')

  GRAPH_REGISTRY[type] = GraphNodeImpl(
    type=type,
    flatten=flatten,
    set_key=set_key,
    pop_key=pop_key,
    create_empty=create_empty,
    clear=clear,
    init=init,
  )

