
def linen_vars_to_nnx_attrs(variables: tp.Mapping[str, Any]) -> dict[str, Any]:
  """Convert a dict of Linen-style variables to NNX variables."""
  nnx_vars = jax.tree_util.tree_map_with_path(
      lambda kp, x: to_nnx_var(get_col_name(kp), x),
      variables,
      is_leaf=lambda x: not isinstance(x, dict),
  )
  flat_paths: dict[tuple, tp.Any] = {}
  for col_name, col_variables in nnx_vars.items():  # pylint: disable=unused-variable
    for path, variable in traversals.flatten_mapping(col_variables).items():
      if path in flat_paths:
        raise ValueError(
            f"Found duplicate variable path {path} with variables "
            f"{flat_paths[path]} and {variable}. "
            "This is not allowed in NNX."
        )
      flat_paths[path] = variable

  nnx_vars = traversals.unflatten_mapping(flat_paths)
  return nnx_vars

