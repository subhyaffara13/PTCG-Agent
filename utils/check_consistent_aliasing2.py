
def check_consistent_aliasing2(
    node: tp.Any,
    prefix: tp.Any,
    /,
    *,
    base_path: tuple[tp.Any, ...] = (),
    node_prefixes: dict[int, list[tuple[PathParts, tp.Any]]],
):
  node_id_to_variable: dict[int, tp.Any] = {}

  for local_path, value in graphlib.iter_graph(node, graph=True):
    path = base_path + local_path
    if isinstance(value, variablelib.Variable):
      value_id = id(value)
      node_id_to_variable[value_id] = value
      # If prefix is a TreeState (e.g. from nnx.prefix(graph=True)),
      # extract the actual prefix value for this Variable using local_path.
      if isinstance(prefix, TreeState):
        prefix_fn = prefix.prefix_fn.value
        if not callable(prefix_fn):
          raise ValueError(
              'When passing a TreeState object as a prefix (e.g. for'
              ' `in_axes`), it must have been produced by `nnx.prefix()` or'
              ' contain a callable in `TreeState.metadata` with signature'
              ' `(path: tuple[Any, ...], value: Variable) -> Any`. Got'
              f' metadata of type {type(prefix_fn).__name__}.'
          )
        leaf_prefix = prefix_fn(local_path, value)
      else:
        leaf_prefix = prefix
      if value_id in node_prefixes:
        node_prefixes[value_id].append((path, leaf_prefix))
      else:
        node_prefixes[value_id] = [(path, leaf_prefix)]

  node_msgs = []
  for node_id, paths_prefixes in node_prefixes.items():
    unique_prefixes = {p for _, p in paths_prefixes}
    if len(unique_prefixes) > 1:
      path_prefix_repr = '\n'.join(
        f'  {"/".join(map(str,path)) if path else "<root>"}: {p}'
        for path, p in paths_prefixes
      )
      if node_id in node_id_to_variable:
        variable = node_id_to_variable[node_id]
        node_type_name = type(variable).__name__
      else:
        node_type_name = f'Node ID: {node_id}'

      node_msgs.append(f'Node: {node_type_name}\n{path_prefix_repr}')

  if node_msgs:
    raise ValueError(
      'Inconsistent aliasing detected. The following nodes have different prefixes:\n'
      + '\n'.join(node_msgs)
    )

