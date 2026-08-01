
def get_composite_save_args(
    pytree: PyTree,
) -> args_lib.Composite:
  return args_lib.Composite(
      state=pytree_checkpoint_handler.PyTreeSaveArgs(pytree)
  )

