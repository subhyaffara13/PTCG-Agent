
def _tree_flatten(
  node: tp.Any,
  nodes: list[NodeDefType[tp.Any]],
  leaves: list[tp.Any],
  paths: list[PathParts] | None,
) -> None:
  seen_variables: dict[int, str] = {}
  seen_refs: dict[int, str] = {}
  def _is_leaf(path, x):
    if isinstance(x, Variable):
      var_id = id(x)
      str_path = jax.tree_util.keystr(path)
      if var_id in seen_variables:
        raise ValueError(
          f'Duplicate {x}\nfound at paths:\n\n'
          f'  - {seen_variables[var_id]}\n'
          f'  - {str_path}\n\n'
          'Tree mode (graph=False) does not support shared references. '
          + _tree_mode_suggestion_api('split')
        )
      seen_variables[var_id] = str_path
      return True
    if variablelib.is_array_ref(x):
      ref_id = id(x)
      str_path = jax.tree_util.keystr(path)
      if ref_id in seen_refs:
        raise ValueError(
          f'Duplicate {x}\nfound at paths:\n\n'
          f'  - {seen_refs[ref_id]}\n'
          f'  - {str_path}\n\n'
          'Tree mode (graph=False) does not support shared references. '
          + _tree_mode_suggestion_api('split')
        )
      seen_refs[ref_id] = str_path
    _check_valid_pytree(x, 'flatten', jax.tree_util.keystr(path))
    return False
  jax_leaves, treedef = jax.tree_util.tree_flatten_with_path(
    node, is_leaf=_is_leaf, is_leaf_takes_path=True
  )
  nnx_paths_and_leaves: list[tuple[PathParts, tp.Any]] = [
    (jax_to_nnx_path(jax_path), value) for jax_path, value in jax_leaves
  ]
  original_indices = {p: i for i, (p, _) in enumerate(nnx_paths_and_leaves)}
  nnx_paths_and_leaves.sort()
  path_index = tuple(
    (p, original_indices[p]) for p, _ in nnx_paths_and_leaves
  )

  tree_nodedef: TreeNodeDef[tp.Any] = TreeNodeDef(
    type=type(node),
    treedef=treedef,
    path_index=path_index,
  )
  nodes.append(tree_nodedef)

  sorted_leaf_index = 0
  for nnx_path, value in nnx_paths_and_leaves:
    if isinstance(value, Variable):
      nodes.append(VariableDef(
        type=value.var_type,
        index=sorted_leaf_index,
        outer_index=None,
        metadata=HashableMapping(value.get_metadata()),
        array_refdef=None,
      ))
    leaves.append(value)
    if paths is not None:
      paths.append(nnx_path)
    sorted_leaf_index += 1

