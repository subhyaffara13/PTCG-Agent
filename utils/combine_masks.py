
def combine_masks(
  *masks: Array | None, dtype: Dtype = jnp.float32
) -> Array | None:
  """Combine attention masks.

  Args:
    *masks: set of attention mask arguments to combine, some can be None.
    dtype: dtype for the returned mask.

  Returns:
    Combined mask, reduced by logical and, returns None if no masks given.
  """
  masks_list = [m for m in masks if m is not None]
  if not masks_list:
    return None
  assert all(
    map(lambda x: x.ndim == masks_list[0].ndim, masks_list)
  ), f'masks must have same rank: {tuple(map(lambda x: x.ndim, masks_list))}'
  mask, *other_masks = masks_list
  for other_mask in other_masks:
    mask = jnp.logical_and(mask, other_mask)
  return mask.astype(dtype)


def combine_masks(
  *masks: Array | None, dtype: Dtype = jnp.float32
) -> Array | None:
  """Combine attention masks.

  Args:
    *masks: set of attention mask arguments to combine, some can be None.
    dtype: dtype for the returned mask.

  Returns:
    Combined mask, reduced by logical and, returns None if no masks given.
  """
  masks_list = [m for m in masks if m is not None]
  if not masks_list:
    return None
  assert all(
    map(lambda x: x.ndim == masks_list[0].ndim, masks_list)
  ), f'masks must have same rank: {tuple(map(lambda x: x.ndim, masks_list))}'
  mask, *other_masks = masks_list
  for other_mask in other_masks:
    mask = jnp.logical_and(mask, other_mask)
  return mask.astype(dtype)

