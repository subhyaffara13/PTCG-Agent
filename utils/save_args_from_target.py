
def save_args_from_target(target: Any) -> Any:
  return jax.tree_util.tree_map(lambda _: ocp.SaveArgs(), target)

