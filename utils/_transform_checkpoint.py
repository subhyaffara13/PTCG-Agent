
def _transform_checkpoint(
    item: PyTree,
    restored: PyTree,
    restore_args: Optional[PyTree],
    transforms: Optional[PyTree],
    transforms_default_to_original: bool,
) -> PyTree:
  """Optionally transforms the restored PyTree to the structure of `item`.

  Args:
    item: a PyTree representing the result structure ("new tree structure").
    restored: a PyTree representing the original tree structure.
    restore_args: tree of RestoreArgs, with the same structure as `item`.
    transforms: provides instructions on how to transform the input trees. See
      transform_utils.
    transforms_default_to_original: See transform_utils.

  Returns:
    A transformed PyTree.
  """
  if item is None:
    if transforms is not None:
      msg = (
          'If providing `transforms`, must provide `item` matching structure'
          ' of expected result.'
      )
      raise ValueError(msg)
    item = restored
  else:
    if transforms is None:
      item = tree_utils.deserialize_tree(restored, item)
    else:
      if restore_args is None:
        raise ValueError(
            'If providing `transforms`, must provide `restore_args` matching'
            ' structure of expected result.'
        )
      transforms = _multi_value_fns_with_args(transforms, restore_args)
      item = transform_utils.apply_transformations(
          restored, transforms, item, transforms_default_to_original
      )
  return item

