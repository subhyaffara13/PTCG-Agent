
def _graph_flatten(
  node: Node,
  node_impl: NodeImpl[Node, Leaf, AuxData] | None,
  path: list[Key] | None,
  ref_index: RefMap,
  ref_outer_index: RefMap | None,
  nodes: list[NodeDefType[tp.Any]],
  attributes: list[tuple[Key, AttrType]],
  leaves: list[tp.Any],
  paths: list[PathParts] | None,
) -> None:
  is_pytree_node_ = type(node_impl) is PytreeNodeImpl

  index: int | None
  if not is_pytree_node_ and node in ref_index:
    nodes.append(NodeRef(index := ref_index[node]))
    return

  is_graph_node_ = type(node_impl) is GraphNodeImpl
  is_variable = isinstance(node, Variable)
  is_array_ref = variablelib.is_array_ref(node)

  # only cache graph nodes, we don't add array refs here
  # as they are added in the make_mutable_arraydef function
  if is_graph_node_ or is_variable:
    index = len(ref_index)
    ref_index[node] = index
  else:
    index = None

  def make_mutable_arraydef(value: variablelib.Ref):
    if value in ref_index:
      index = ref_index[value]
      return NodeRef(index), REPEATED
    else:
      index = len(ref_index)
      ref_index[value] = index
    output_value: NoUpdate | ArrayRefOutput | variablelib.Ref
    if ref_outer_index is not None:
      if value in ref_outer_index:
        outer_index = ref_outer_index[value]
        output_value = NO_UPDATE
        array_refdef = ArrayRefDef(index=index, outer_index=outer_index)
      else:
        output_value = ArrayRefOutput(value[...])
        array_refdef = ArrayRefDef(index=index, outer_index=None)
    else:
      output_value = value
      array_refdef = ArrayRefDef(index=index, outer_index=None)
    return array_refdef, output_value

  if is_variable:
    assert isinstance(node, Variable)
    assert index is not None
    prev_inner_value = node.get_raw_value()
    if variablelib.is_array_ref(prev_inner_value):
      array_refdef, inner_value = make_mutable_arraydef(prev_inner_value)
    else:
      array_refdef = None
      inner_value = prev_inner_value
    if path is None:
      leaf = inner_value
    else:
      leaf = node  # type: ignore[assignment]
      if inner_value is not prev_inner_value:
        leaf.set_raw_value(inner_value)

    variabledef = VariableDef(
      type=node.var_type,  # type: ignore
      index=index,
      outer_index=ref_outer_index.get(node, None) if ref_outer_index else None,
      metadata=HashableMapping(node.get_metadata()),
      array_refdef=array_refdef,
    )
    if type(inner_value) is not Repeated:
      assert not isinstance(leaf, Repeated)
      leaves.append(leaf)
      if path is not None:
        assert paths is not None
        paths.append(tuple(path))
    nodes.append(variabledef)
    return
  elif is_array_ref:
    array_refdef, leaf = make_mutable_arraydef(node)  # type: ignore[arg-type]
    if not isinstance(leaf, Repeated):
      leaves.append(leaf)
      if path is not None:
        assert paths is not None
        paths.append(tuple(path))
    nodes.append(array_refdef)
    return
  elif not is_pytree_node_ and not is_graph_node_:
    # unkown leaf
    leaves.append(node)
    if path is not None:
      assert paths is not None
      paths.append(tuple(path))
    return

  if node_impl is None:
    raise RuntimeError(f'Unsupported type: {type(node)}, this is a bug.')

  values, metadata = node_impl.flatten(node)
  num_attributes = len(values)
  nodedef = NodeDef(
    node_impl.type,
    index,
    ref_outer_index[node]
    if is_graph_node_ and ref_outer_index and node in ref_outer_index
    else None,
    num_attributes,
    metadata,
  )
  nodes.append(nodedef)

  for key, value in values:
    is_data = None
    if isinstance(value, DataElem):
      value = value.value
      is_data = True
    elif isinstance(value, StaticElem):
      value = value.value
      is_data = False

    if is_data is False:
      attributes.append((key, Static(value)))
      continue

    value_node_impl = get_node_impl(value)
    if path is not None:
      path.append(key)
    if value_node_impl is not None or isinstance(value, Variable):
      attributes.append((key, NODE_ATTR))
      _graph_flatten(
        value,
        value_node_impl,
        path,
        ref_index,
        ref_outer_index,
        nodes,
        attributes,
        leaves,
        paths,
      )
    elif variablelib.is_array_ref(value):
      attributes.append((key, NODE_ATTR))
      array_refdef, leaf = make_mutable_arraydef(value)
      if not isinstance(leaf, Repeated):
        leaves.append(leaf)
        if paths is not None:
          paths.append(tuple(path))  # type: ignore
      nodes.append(array_refdef)
    elif isinstance(value, (jax.Array, np.ndarray)) or is_data:
      attributes.append((key, LEAF_ATTR))
      if paths is not None:
        paths.append(tuple(path))  # type: ignore
      leaves.append(value)
    else:
      attributes.append((key, Static(value)))

    if path is not None:
      path.pop()

  return

