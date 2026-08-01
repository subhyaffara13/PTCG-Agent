
def _fill_missing_save_or_restore_args(
    item: PyTree, args: Optional[PyTree], *, mode: str
) -> PyTree:
  """Fills in missing values in the tree of SaveArgs or RestoreArgs.

  Values may be "missing" because of empty nodes in `item`. After returning, all
  keys in `item`, with empty nodes or not, will have a corresponding value
  in the result.

  Args:
    item: tree to save or target to restore.
    args: tree of SaveArgs or RestoreArgs. May be None, if the user did not
      provide it.
    mode: 'save' or 'restore'.

  Returns:
    A tree of SaveArgs or RestoreArgs with missing values filled in.
  """

  # Because of empty states, the user-provided args may not contain
  # all necessary arguments. These should be filled in with default args.
  def _maybe_set_default_save_restore_args(v, leaf_args):
    if mode == 'save':
      return leaf_args if isinstance(leaf_args, SaveArgs) else SaveArgs()
    if mode == 'restore':
      if isinstance(leaf_args, ArrayRestoreArgs):
        return _update_array_restore_args(v, leaf_args)
      return leaf_args if isinstance(leaf_args, RestoreArgs) else RestoreArgs()
    raise ValueError(f'Unknown mode: {mode}.')

  return jax.tree_util.tree_map(
      _maybe_set_default_save_restore_args,
      item,
      item if args is None else args,
      is_leaf=utils.is_empty_or_leaf,
  )

