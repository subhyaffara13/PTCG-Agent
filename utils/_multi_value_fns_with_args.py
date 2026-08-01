
def _multi_value_fns_with_args(
    transforms: PyTree, restore_args: PyTree
) -> PyTree:
  """Constructs a wrapper for multi_value_fn including RestoreArgs."""
  flat_restore_args = tree_utils.to_flat_dict(restore_args, sep='/')

  def _maybe_wrap_transform(transform: Transform):
    def _multi_value_fn_with_args(transform_key: str, tree: PyTree) -> Any:
      nonlocal transform
      transform = typing.cast(RestoreTransform, transform)
      return transform.multi_value_fn(
          transform_key, tree, flat_restore_args[transform_key]
      )

    if transform.multi_value_fn is not None:
      return Transform(multi_value_fn=_multi_value_fn_with_args)
    else:
      return transform

  return jax.tree.map(_maybe_wrap_transform, transforms)

