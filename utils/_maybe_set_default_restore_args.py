
def _maybe_set_default_restore_args(args):
  if isinstance(args, RestoreArgs):
    return args
  return RestoreArgs(restore_type=None)

