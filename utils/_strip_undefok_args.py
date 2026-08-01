
def _strip_undefok_args(undefok, args):
  """Returns a new list of args after removing flags in --undefok."""
  if undefok:
    undefok_names = {name.strip() for name in undefok.split(',')}
    undefok_names |= {'no' + name for name in undefok_names}
    # Remove undefok flags.
    args = [arg for arg in args if not _is_undefok(arg, undefok_names)]
  return args

