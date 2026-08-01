
def _collect_stats(
  node: tp.Any, node_stats: dict[int, dict[type[Variable], SizeBytes]]
):
  if not graphlib.is_node(node) and not isinstance(node, Variable):
    raise ValueError(f'Expected a graph node or Variable, got {type(node)!r}.')

  if id(node) in node_stats:
    return

  stats: dict[type[Variable], SizeBytes] = {}
  node_stats[id(node)] = stats

  if isinstance(node, Variable):
    var_type = node.var_type
    if issubclass(var_type, nnx.RngState):
      var_type = nnx.RngState
    size_bytes = SizeBytes.from_any(node.get_raw_value())
    if size_bytes:
      stats[var_type] = size_bytes

  else:
    node_impl = graphlib.get_node_impl(node)
    assert node_impl is not None
    node_dict = node_impl.node_dict(node)
    for key, value in node_dict.items():
      if id(value) in node_stats:
        continue
      if graphlib.is_node(value) or isinstance(value, Variable):
        _collect_stats(value, node_stats)
        child_stats = node_stats[id(value)]
        for var_type, size_bytes in child_stats.items():
          if var_type in stats:
            stats[var_type] += size_bytes
          else:
            stats[var_type] = size_bytes


def _collect_stats(
  path: statelib.PathParts,
  node: tp.Any,
  node_stats: NodeStats,
  object_types: set[type],
):
  if not graphlib.is_node(node) and not isinstance(node, variablelib.Variable):
    raise ValueError(f'Expected a graph node or Variable, got {type(node)!r}.')

  if id(node) in node_stats:
    return

  stats: dict[type[variablelib.Variable], SizeBytes] = {}
  variable_groups: defaultdict[
    type[variablelib.Variable], defaultdict[typing.Key, variablelib.Variable]
  ] = defaultdict(lambda: defaultdict())
  node_stats[id(node)] = ObjectInfo(path, stats, variable_groups)

  if isinstance(node, nnx.Pytree):
    node._nnx_tabulate_id = id(node)  # type: ignore
    object_types.add(type(node))

  node_impl = graphlib.get_node_impl(node)
  assert node_impl is not None
  node_dict = node_impl.node_dict(node)
  for key, value in node_dict.items():
    if id(value) in node_stats:
      continue
    elif isinstance(value, variablelib.Variable):
      var_type = type(value)
      if issubclass(var_type, nnx.RngState):
        var_type = nnx.RngState
      size_bytes = SizeBytes.from_any(value.get_value())
      if var_type in stats:
        stats[var_type] += size_bytes
      else:
        stats[var_type] = size_bytes
      variable_groups[var_type][key] = value
      node_stats[id(value)] = None
    elif graphlib.is_node(value):
      _collect_stats((*path, key), value, node_stats, object_types)
      # accumulate stats from children
      child_info = node_stats[id(value)]
      assert child_info is not None
      for var_type, size_bytes in child_info.stats.items():
        if var_type in stats:
          stats[var_type] += size_bytes
        else:
          stats[var_type] = size_bytes

