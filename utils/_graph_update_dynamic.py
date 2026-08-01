
def _graph_update_dynamic(node: tp.Any, state: tp.Mapping[KeyT, tp.Any]):
  def _update_variable(node: Variable, value):
    if isinstance(value, Variable):
      # updated from Variable
      node.update_from_state(value)
    else:
      # updated from raw value
      if isinstance(value, State) and not value:
        # NOTE: this is a special case when trying to update a Variable from state
        # created when flattening into a NodeRef, which creates an empty State. This
        # can happen when using standalone Variables with `grad`
        pass
      else:
        if is_array_ref(node.get_raw_value()) and (
          isinstance(value, jax.Array) or is_array_ref(value)
        ):
          node[...] = value[...]
        else:
          node.set_raw_value(value, _unsafe_bypass_check=True)

  if isinstance(node, Variable):
    _update_variable(node, state)
    return

  if not is_node(node):
    raise RuntimeError(f'Unsupported type: {type(node)}')

  node_impl = get_node_impl(node)
  if node_impl is None:
    raise TypeError(f'Unknown node type: {type(node)}')
  node_dict = node_impl.node_dict(node)
  for key, value in state.items():
    # case 1: new state is being added
    if key not in node_dict:
      if node_impl.set_key is None:
        raise ValueError(
          f'Cannot set key {key!r} on immutable node of '
          f'type {type(node).__name__}'
        )
      if isinstance(value, Variable):
        copy_ref = not isinstance(
          value.get_raw_value(), (NoUpdate, Repeated, ArrayRefOutput)
        )
        value = value.copy(_copy_ref=copy_ref)
      node_impl.set_key(node, key, value)
      continue

    current_value = node_dict[key]

    # case 2: subgraph is being updated
    if is_array_ref(current_value):
      current_value[...] = value
    elif is_node(current_value):
      if is_node_leaf(value):
        raise ValueError(f'Expected a subgraph for {key!r}, but got: {value!r}')
      _graph_update_dynamic(current_value, value)
    elif isinstance(current_value, Variable):
      _update_variable(current_value, value)
    elif node_impl.set_key is not None:
      node_impl.set_key(node, key, value)
    else:
      raise ValueError(
        f'Cannot set key {key!r} on immutable node of '
        f'type {type(node).__name__}'
      )

