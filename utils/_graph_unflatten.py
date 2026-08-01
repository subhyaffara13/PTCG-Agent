
def _graph_unflatten(
  nodedef: NodeDefType[Node],
  node_impl: NodeImpl[Node, Leaf, AuxData] | None,
  node_iter: tp.Iterator[NodeDefType[Node]],
  attribute_iter: tp.Iterator[tuple[Key, AttrType]],
  leaves_iter: tp.Iterator[tp.Any],
  index_ref: IndexMap,
  outer_index_outer_ref: IndexMap | None,
  copy_variables: bool,
  recreate_variables: bool
) -> Node:
  """Recursive helper for graph_unflatten.

    Args:
      nodedef: A GraphDef instance or an index to a node in the cache.
      state: A mapping from attribute names to variables or subgraphs.
      index_ref: A mapping from indexes to nodes that have been traversed.
        If a node is already in the cache, it won't be traversed again.
      outer_index_outer_ref: A mapping from indexes to existing nodes that can be reused.
        When an reference is reused, ``GraphNodeImpl.clear`` is called to leave the
        object in an empty state and then filled by the unflatten process, as a result
        existing graph nodes are mutated to have the new content/topology
        specified by the nodedef.
  """

  def get_mutable_array(array_refdef: ArrayRefDef, leaf):
    assert type(array_refdef) is ArrayRefDef
    if (
      outer_index_outer_ref is not None
      and array_refdef.outer_index is not None
      and array_refdef.outer_index in outer_index_outer_ref
    ):
      # if array ref exists, update it
      array_ref = outer_index_outer_ref[array_refdef.outer_index]
      if not variablelib.is_array_ref(array_ref):
        raise RuntimeError(f'Expected a ArrayRef type but got {array_ref}.')
      if type(leaf) is not NoUpdate:
        raise RuntimeError(f'Expected a no update for ArrayRef but got {leaf}.')
    elif type(leaf) in (NoUpdate, Repeated):
      raise ValueError(
        f"Expected a ArrayRefOutput type but got '{leaf}.'"
      )
    elif type(leaf) is ArrayRefOutput:
      array_ref = jax.new_ref(leaf.value)
    elif variablelib.is_array_ref(leaf):
      array_ref = leaf
    else:
      # here we allow merging frozen arrays and will not create a new array ref
      array_ref = leaf

    index_ref[array_refdef.index] = array_ref
    return array_ref

  if type(nodedef) is NodeRef:
    return index_ref[nodedef.index]

  if type(nodedef) is VariableDef:
    variabledef = tp.cast(VariableDef[Variable], nodedef)
    # its a unseen variable, create a new one

    if variabledef.array_refdef is not None:
      if type(variabledef.array_refdef) is NodeRef:
        value = index_ref[variabledef.array_refdef.index]
      else:
        value = next(leaves_iter)
        assert type(variabledef.array_refdef) is ArrayRefDef
        if isinstance(value, Variable):
          copy_ref = not isinstance(
            value.get_raw_value(), (NoUpdate, Repeated, ArrayRefOutput)
          )
          value = value.copy(_copy_ref=copy_ref) if copy_variables else value
          inner_value = value.get_raw_value()
          array_ref = get_mutable_array(variabledef.array_refdef, inner_value)
          if array_ref is not inner_value:
            value.set_raw_value(array_ref)
        else:
          # if value is an array or array ref, we need call get_mutable_array
          # to register it in the index_ref
          value = get_mutable_array(variabledef.array_refdef, value)
    else:
      value = next(leaves_iter)
      if isinstance(value, Variable) and copy_variables:
        copy_ref = not isinstance(
          value.get_raw_value(), (NoUpdate, Repeated, ArrayRefOutput)
        )
        value = value.copy(_copy_ref=copy_ref)

    # when idxmap is present, check if the Varable exists there
    # and update existing variables if it does
    if (
      outer_index_outer_ref is not None
      and variabledef.outer_index is not None
      and variabledef.outer_index in outer_index_outer_ref
    ):
      # if variable exists, update it
      variable = outer_index_outer_ref[variabledef.outer_index]
      if not isinstance(variable, Variable):
        raise ValueError(f'Expected a Variable type but got {type(variable)}.')
      elif isinstance(value, Variable):
        variable.update_from_state(value)
      else:
        variable.set_raw_value(value)
    else:  # variabledef.index not in index_ref_cache
      # variable reference does not exist outside, create a new one
      if isinstance(value, Variable) or not recreate_variables:
        variable = value
      else:
        variable = variabledef.type.from_metadata(
          value, dict(variabledef.metadata)
        )
    index_ref[variabledef.index] = variable
    return variable  # type: ignore[return-value]

  if type(nodedef) is ArrayRefDef:
    leaf = next(leaves_iter)
    array_ref = get_mutable_array(nodedef, leaf)
    return array_ref  # type: ignore[return-value]

  assert type(nodedef) is NodeDef
  if node_impl is None:
    raise RuntimeError(f'Unsupported type: {nodedef.type}, this is a bug.')
  if nodedef.index is not None and nodedef.index in index_ref:
    raise RuntimeError(f'GraphDef index {nodedef.index} already used.')

  def _get_children() -> list[tuple[Key, tp.Any]]:
    children: list[tuple[Key, LeafType | Node]] = []  # type: ignore[invalid-annotation]

    assert type(nodedef) is NodeDef
    for _ in range(nodedef.num_attributes):
      key, value = next(attribute_iter)
      if type(value) is Static:
        children.append((key, value.value))  # type: ignore[attribute-error]
      elif type(value) is LeafAttr:
        leaf = next(leaves_iter)
        children.append((key, leaf))
      elif type(value) is NodeAttr:
        node_def = next(node_iter)
        if isinstance(node_def, NodeRef):
          node = index_ref[node_def.index]
        elif isinstance(node_def, ArrayRefDef):
          leaf = next(leaves_iter)
          node = get_mutable_array(node_def, leaf)
        elif isinstance(node_def, NodeDef | VariableDef):
          value_node_impl = get_node_impl_for_type(node_def.type)
          node = _graph_unflatten(
            node_def,
            value_node_impl,
            node_iter,
            attribute_iter,
            leaves_iter,
            index_ref,
            outer_index_outer_ref,
            copy_variables,
            recreate_variables
          )
        else:
          raise RuntimeError(f'Unknown node definition: {node_def!r}')
        children.append((key, node))
      elif type(value) is NodeRef:
        children.append((key, index_ref[value.index]))  # type: ignore[attribute-error]
      else:
        raise RuntimeError(f'Unknown static field: {key!r}')

    return children

  if isinstance(node_impl, GraphNodeImpl):
    # we create an empty node first and add it to the index
    # this avoids infinite recursion when there is a reference cycle
    assert type(nodedef) is NodeDef
    if (
      outer_index_outer_ref is not None
      and nodedef.outer_index is not None
      and nodedef.outer_index in outer_index_outer_ref
    ):
      node = outer_index_outer_ref[nodedef.outer_index]
      if type(node) != nodedef.type:
        raise ValueError(
          f'Expected a node of type {nodedef.type} for index '
          f'{nodedef.index}, but got a node of type {type(node)}.'
        )
      node_impl.clear(node)
    else:
      node = node_impl.create_empty(nodedef.metadata)
    assert nodedef.index is not None
    index_ref[nodedef.index] = node
    node_impl.init(node, _get_children())
  else:
    # if the node type does not support the creation of an empty object it means
    # that it cannot reference itself, so we can create its children first
    node = node_impl.unflatten(_get_children(), nodedef.metadata)

  return node

