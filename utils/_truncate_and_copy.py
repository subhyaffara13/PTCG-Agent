
def _truncate_and_copy(
    array_source: np.ndarray,
    array_dest: np.ndarray,
    prefix_slices: tuple[slice, ...],
    remaining_edge_items_per_axis: tuple[int | None, ...],
) -> None:
  """Recursively copy values along the edges of a source into a destination.

  This function mutates the destination array in place, copying parts of input
  array into them, so that it contains a truncated versions of the original
  array.

  Args:
    array_source: Source array, which we will truncate.
    array_dest: Destination array, whose axis sizes will be either the same as
      `array_source` or of size `2 * edge_items + 1` depending on the
      truncation.
    prefix_slices: Prefix of slices for the source and destination.
    remaining_edge_items_per_axis: Number of edge items to keep for each axis,
      ignoring any axes whose slices are already computed in `source_slices`.
  """
  if not remaining_edge_items_per_axis:
    # Perform the base case slice.
    assert (
        len(prefix_slices) == len(array_source.shape) == len(array_dest.shape)
    )
    array_dest[prefix_slices] = array_source[prefix_slices]
  else:
    # Recursive step.
    axis = len(prefix_slices)
    edge_items = remaining_edge_items_per_axis[0]
    if edge_items is None:
      # Don't need to slice.
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(None),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )
    else:
      assert array_source.shape[axis] > 2 * edge_items
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(None, edge_items),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(-edge_items, None),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )


def _truncate_and_copy(
    array_source: torch.Tensor,
    array_dest: np.ndarray,
    prefix_slices: tuple[slice, ...],
    remaining_edge_items_per_axis: tuple[int | None, ...],
) -> None:
  """Recursively copy values on the edges of a torch tensor into a numpy array.

  This function mutates the destination array in place, copying parts of input
  array into them, so that it contains a truncated versions of the original
  array.

  Args:
    array_source: Source array, which we will truncate.
    array_dest: Destination array, whose axis sizes will be either the same as
      `array_source` or of size `2 * edge_items + 1` depending on the
      truncation.
    prefix_slices: Prefix of slices for the source and destination.
    remaining_edge_items_per_axis: Number of edge items to keep for each axis,
      ignoring any axes whose slices are already computed in `source_slices`.
  """
  assert torch is not None, "PyTorch is not available."
  if not remaining_edge_items_per_axis:
    # Perform the base case slice.
    assert (
        len(prefix_slices) == len(array_source.shape) == len(array_dest.shape)
    )
    array_dest[prefix_slices] = _tensor_to_numpy(array_source[prefix_slices])
  else:
    # Recursive step.
    axis = len(prefix_slices)
    edge_items = remaining_edge_items_per_axis[0]
    if edge_items is None:
      # Don't need to slice.
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(None),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )
    else:
      assert array_source.shape[axis] > 2 * edge_items
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(None, edge_items),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )
      _truncate_and_copy(
          array_source=array_source,
          array_dest=array_dest,
          prefix_slices=prefix_slices + (slice(-edge_items, None),),
          remaining_edge_items_per_axis=remaining_edge_items_per_axis[1:],
      )

