
def _check_error(error, *, debug=False):
  if any(map(np.shape, error._pred.values())):
    error = _reduce_any_error(error)
  err_args, tree_def = tree_flatten(error)

  return check_p.bind(*err_args, err_tree=tree_def, debug=debug)


def _check_error(err: checkify.Error) -> None:
  """Checks the error and converts it to chex format."""
  try:
    checkify.check_error(err)
  except ValueError as exc:
    msg = str(exc)
    if _chexify_error_pattern.match(msg):
      # Remove internal code pointers.
      internal_info_pos = msg.rfind('(check failed at')
      if internal_info_pos != -1:
        msg = msg[:internal_info_pos]
      raise AssertionError(msg)  # pylint:disable=raise-missing-from
    else:
      raise

