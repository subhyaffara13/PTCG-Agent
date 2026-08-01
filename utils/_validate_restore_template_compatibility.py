
def _validate_restore_template_compatibility(
    *,
    item: PyTree,
    restore_args: PyTree,
) -> None:
  """Checks explicit restore_args do not conflict with the restore item."""
  item_leaves = jax.tree.leaves(item, is_leaf=_is_restore_spec_leaf)
  restore_arg_leaves = jax.tree.leaves(
      restore_args, is_leaf=_is_restore_spec_leaf
  )
  for index, (item_leaf, restore_arg_leaf) in enumerate(
      zip(item_leaves, restore_arg_leaves)
  ):
    item_expected = _expected_leaf_from_template(item_leaf)
    restore_arg_expected = _expected_leaf_from_template(restore_arg_leaf)
    if item_expected is None or restore_arg_expected is None:
      continue
    if (
        restore_arg_expected.shape is not None
        and item_expected.shape is not None
        and restore_arg_expected.shape != item_expected.shape
    ):
      raise ValueError(
          'colocated restore does not support restore_args shape transforms; '
          'item and restore_args shape must agree. '
          f'leaf={index}, item_shape={item_expected.shape}, '
          f'restore_args_shape={restore_arg_expected.shape}.'
      )
    if (
        restore_arg_expected.dtype is not None
        and item_expected.dtype is not None
        and restore_arg_expected.dtype != item_expected.dtype
    ):
      raise ValueError(
          'colocated restore does not support restore_args dtype casting; '
          'item and restore_args dtype must agree. '
          f'leaf={index}, item_dtype={item_expected.dtype}, '
          f'restore_args_dtype={restore_arg_expected.dtype}.'
      )

