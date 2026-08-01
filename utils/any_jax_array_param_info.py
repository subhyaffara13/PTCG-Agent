
def any_jax_array_param_info(param_infos: Pytree) -> types.ParamInfo | None:
  """Returns any jax.Array param_info in the PyTree, or None."""
  return jax.tree_util.tree_reduce(
      lambda found_jax_array, param_info: (
          found_jax_array
          or (param_info if represents_jax_array(param_info) else None)
      ),
      tree=param_infos,
      initializer=None,
  )

