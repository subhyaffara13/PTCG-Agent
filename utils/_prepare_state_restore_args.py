
def _prepare_state_restore_args(
    state: args_lib.PyTreeRestore,
) -> args_lib.PyTreeRestore:
  """Ensures restore_args are populated and converted to ArrayRestoreArgs."""
  if state.item is None:
    return state

  restore_args = jax.tree.map(
      lambda x: type_handlers.ArrayRestoreArgs(sharding=x.sharding)
      if isinstance(x, jax.ShapeDtypeStruct)
      else checkpoint_utils.construct_restore_args(x),
      state.item,
  )

  return args_lib.PyTreeRestore(item=state.item, restore_args=restore_args)

