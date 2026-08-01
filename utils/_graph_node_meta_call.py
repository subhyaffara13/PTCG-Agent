
def _graph_node_meta_call(cls: tp.Type[P], *args, **kwargs) -> P:
  node = cls.__new__(cls, *args, **kwargs)
  object.__setattr__(node, '_pytree__state', PytreeState())
  object.__setattr__(node, '_pytree__nodes', cls._pytree__nodes)
  cls._pytree_meta_construct(node, *args, **kwargs)
  if cls._pytree__is_pytree:
    missing: dict[str, bool] = {}
    for name, value in vars(node).items():
      if name not in node._pytree__nodes:
        missing[name] = is_data(value)
    if missing:
      object.__setattr__(
        node, '_pytree__nodes', node._pytree__nodes.update(missing)
      )
    check_pytree(node)

  return node

