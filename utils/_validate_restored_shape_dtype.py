
def _validate_restored_shape_dtype(
    *,
    restored_state: PyTree,
    template_state: PyTree,
) -> None:
  """Validates restored leaves against caller-provided shape/dtype specs."""
  restored_leaves = jax.tree.leaves(restored_state)
  template_leaves = jax.tree.leaves(
      template_state, is_leaf=_is_restore_spec_leaf
  )
  if len(restored_leaves) != len(template_leaves):
    raise ValueError(
        'colocated restore produced a different number of leaves than the '
        f'restore template: restored={len(restored_leaves)}, '
        f'template={len(template_leaves)}.'
    )

  for index, (restored_leaf, template_leaf) in enumerate(
      zip(restored_leaves, template_leaves)
  ):
    expected_leaf = _expected_leaf_from_template(template_leaf)
    if expected_leaf is None:
      continue
    restored_shape = getattr(restored_leaf, 'shape', None)
    if (
        expected_leaf.shape is not None
        and tuple(restored_shape or ()) != expected_leaf.shape
    ):
      raise ValueError(
          'colocated restore produced a leaf with an unexpected shape: '
          f'leaf={index}, restored_shape={restored_shape}, '
          f'expected_shape={expected_leaf.shape}.'
      )
    restored_dtype = getattr(restored_leaf, 'dtype', None)
    if (
        expected_leaf.dtype is not None
        and restored_dtype != expected_leaf.dtype
    ):
      raise ValueError(
          'colocated restore produced a leaf with an unexpected dtype: '
          f'leaf={index}, restored_dtype={restored_dtype}, '
          f'expected_dtype={expected_leaf.dtype}.'
      )

