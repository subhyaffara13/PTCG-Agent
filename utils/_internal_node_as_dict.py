
def _internal_node_as_dict(x: Any) -> Mapping[str, Any]:
  keys_and_children, _ = tree_flatten_with_path_one_level(x)
  return {jax.tree_util.keystr(k): v for k, v in keys_and_children}

