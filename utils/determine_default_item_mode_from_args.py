
def determine_default_item_mode_from_args(
    args: args_lib.CheckpointArgs,
) -> bool:
  if isinstance(args, args_lib.Composite):
    return False
  else:
    return True

