
def check_consistent_aliasing(
  node: tp.Any,
  prefix: tp.Any,
  /,
  *,
  node_prefixes: dict[int, list[tuple[PathParts, tp.Any]]] | None = None,
):
  """Check for consistent aliasing of nodes when extracting graph."""
  if node_prefixes is None:
    node_prefixes = {}

  # Store variable references for error messages
  node_id_to_variable: dict[int, tp.Any] = {}

  # collect all paths and prefixes for each node
  for path, value in graphlib.iter_graph(node, graph=True):
    if graphlib.is_graph_node(value) or isinstance(value, graphlib.Variable):
      if isinstance(value, Pytree):
        value._check_valid_context(
          lambda: f'Trying to extract graph node from different trace level, got {value!r}'
        )
      if isinstance(value, graphlib.Variable):
        if not value._can_update:
          raise ValueError(
            f'Cannot extract graph node from different trace level, got {value!r}'
          )
        if isinstance(prefix, PrefixMapping):
          variable_prefix = prefix.map_prefix(path, value)
        else:
          variable_prefix = prefix

        value_id = id(value)
        node_id_to_variable[value_id] = value
        if value_id in node_prefixes:
          paths_prefixes = node_prefixes[value_id]
          paths_prefixes.append((path, variable_prefix))
        else:
          node_prefixes[value_id] = [(path, variable_prefix)]

  # check for inconsistent aliasing
  node_msgs = []
  for node_id, paths_prefixes in node_prefixes.items():
    unique_prefixes = {prefix for _, prefix in paths_prefixes}
    if len(unique_prefixes) > 1:
      path_prefix_repr = '\n'.join(
        f'  {"/".join(map(str,path)) if path else "<root>"}: {prefix}'
        for path, prefix in paths_prefixes
      )
      # Get the variable type name if available
      if node_id in node_id_to_variable:
        variable = node_id_to_variable[node_id]
        node_type_name = type(variable).__name__
      else:
        node_type_name = f'Node ID: {node_id}'

      nodes_msg = f'Node: {node_type_name}\n{path_prefix_repr}'
      node_msgs.append(nodes_msg)

  if node_msgs:
    raise ValueError(
      'Inconsistent aliasing detected. The following nodes have different prefixes:\n'
      + '\n'.join(node_msgs)
    )

