
def _truncate_part_with_slices(
    array: jax.Array,
    mask: jax.Array,
    prefix_slices: tuple[slice, ...],
    remaining_edge_items_per_axis: tuple[int | None, ...],
    xnp=None,
) -> tuple[jax.Array, jax.Array]:
  """Helper to truncate names of an array.

  Args:
    array: An array to truncate.
    mask: Mask array, which must be broadcastable to `array`.
    prefix_slices: Slices to apply to each axis of `array` and `mask`, starting
      at axis 0, which we have already computed.
    remaining_edge_items_per_axis: Number of edge items to keep for each axis,
      ignoring any axes whose slices are already computed in `prefix_slices`.
    xnp: backend to use (numpy or jax.numpy).

  Returns:
    Truncated array and mask, which will both be the same shape.
  """
  if xnp is None:
    assert jax is not None, "JAX is not available."
    xnp = jax.numpy

  array = xnp.array(array)
  mask = xnp.array(mask)
  mask = xnp.broadcast_to(mask, array.shape)
  if not remaining_edge_items_per_axis:
    # Perform the base case slice.
    assert len(prefix_slices) == len(array.shape)
    truncated_array = array[prefix_slices]

    valid_mask_slices = tuple(
        slice(None) if mask.shape[i] == 1 else array_slice
        for i, array_slice in enumerate(prefix_slices)
    )
    truncated_mask = xnp.broadcast_to(
        xnp.array(mask[valid_mask_slices]), truncated_array.shape
    )
    return truncated_array, truncated_mask

  # Recursive step: extract one name, run the function on each side, and
  # concatenate.
  axis = len(prefix_slices)
  edge_items = remaining_edge_items_per_axis[0]
  if edge_items is None:
    # Don't need to slice.
    return _truncate_part_with_slices(
        array,
        mask,
        prefix_slices=prefix_slices + (slice(None),),
        remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
        xnp=xnp,
    )
  else:
    assert array.shape[axis] > 2 * edge_items
    result_a, valid_a = _truncate_part_with_slices(
        array,
        mask,
        prefix_slices=prefix_slices + (slice(None, edge_items),),
        remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
        xnp=xnp,
    )
    result_b, valid_b = _truncate_part_with_slices(
        array,
        mask,
        prefix_slices=prefix_slices + (slice(-edge_items, None),),
        remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
        xnp=xnp,
    )
    padding_shape = list(result_a.shape)
    padding_shape[axis] = 1
    result = xnp.concatenate(
        [result_a, xnp.zeros(padding_shape, result_a.dtype), result_b],
        axis=axis,
    )
    valid = xnp.concatenate(
        [valid_a, xnp.zeros(padding_shape, valid_a.dtype), valid_b], axis=axis
    )
    return result, valid

