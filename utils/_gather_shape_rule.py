
def _gather_shape_rule(operand, indices, *, dimension_numbers,
                       slice_sizes, unique_indices, indices_are_sorted,
                       mode, fill_value):
  """Validates the well-formedness of the arguments to Gather.

  The code implements the checks based on the detailed operation semantics of
  XLA's `Gather <https://www.openxla.org/xla/operation_semantics#gather>`_
  operator and following the outline of the implementation of
  ShapeInference::InferGatherShape in TensorFlow.
  """

  offset_dims = dimension_numbers.offset_dims
  collapsed_slice_dims = dimension_numbers.collapsed_slice_dims
  operand_batching_dims = dimension_numbers.operand_batching_dims
  start_indices_batching_dims = dimension_numbers.start_indices_batching_dims
  start_index_map = dimension_numbers.start_index_map

  # Note: in JAX, index_vector_dim is always computed as below, cf. the
  # documentation of the GatherDimensionNumbers class.
  index_vector_dim = _rank(indices) - 1

  # This case should never happen in JAX, due to the implicit construction of
  # index_vector_dim, but is included for completeness.
  if _rank(indices) < index_vector_dim or index_vector_dim < 0:
    raise TypeError(f"Gather index leaf dimension must be within [0, rank("
                    f"indices) + 1). rank(indices) is {_rank(indices)} and "
                    f"gather index leaf dimension is {index_vector_dim}.")

  # Start ValidateGatherDimensions
  # In the error messages output by XLA, "offset_dims" is called "Output window
  # dimensions" in error messages. For consistency's sake, our error messages
  # stick to "offset_dims".
  _is_sorted(offset_dims, "gather", "offset_dims")
  _no_duplicate_dims(offset_dims, "gather", "offset_dims")

  output_offset_dim_count = len(offset_dims)
  output_shape_rank = len(offset_dims) + _rank(indices) - 1

  for i in range(output_offset_dim_count):
    offset_dim = offset_dims[i]
    if offset_dim < 0 or offset_dim >= output_shape_rank:
      raise TypeError(f"Offset dimension {i} in gather op is out of bounds; "
                      f"got {offset_dim}, but should have been in "
                      f"[0, {output_shape_rank})")

  if len(start_index_map) != indices.shape[index_vector_dim]:
    raise TypeError(f"Gather op has {len(start_index_map)} elements in "
                    f"start_index_map and the bound of dimension "
                    f"{index_vector_dim=} of indices is "
                    f"{indices.shape[index_vector_dim]}. These two "
                    f"numbers must be equal.")

  for i in range(len(start_index_map)):
    operand_dim_for_start_index_i = start_index_map[i]
    if (operand_dim_for_start_index_i < 0 or
        operand_dim_for_start_index_i >= _rank(operand)):
      raise TypeError(f"Invalid start_index_map; domain is "
                      f"[0, {_rank(operand)}), got: "
                      f"{i}->{operand_dim_for_start_index_i}.")

  _no_duplicate_dims(start_index_map, "gather", "start_index_map")

  # _is_sorted and _sorted_dims_in_range are checked in the opposite order
  # compared to the XLA implementation. In cases when the input is not sorted
  # AND there are problematic collapsed_slice_dims, the error message will thus
  # be different.
  _is_sorted(collapsed_slice_dims, "gather", "collapsed_slice_dims")
  _sorted_dims_in_range(collapsed_slice_dims, _rank(operand), "gather",
                        "collapsed_slice_dims")
  _no_duplicate_dims(collapsed_slice_dims, "gather", "collapsed_slice_dims")

  _no_duplicate_dims(operand_batching_dims, "gather", "operand_batching_dims")
  _is_sorted(operand_batching_dims, "gather", "operand_batching_dims")
  _sorted_dims_in_range(
      operand_batching_dims, _rank(operand), "gather", "operand_batching_dims"
  )

  _disjoint_dims(collapsed_slice_dims, operand_batching_dims, "gather",
                 "collapsed_slice_dims", "operand_batching_dims")
  _disjoint_dims(start_index_map, operand_batching_dims, "gather",
                 "start_index_map", "operand_batching_dims")

  _no_duplicate_dims(
      start_indices_batching_dims, "gather", "start_indices_batching_dims"
  )
  _dims_in_range(
      start_indices_batching_dims,
      _rank(indices),
      "gather",
      "start_indices_batching_dims",
  )
  if index_vector_dim in start_indices_batching_dims:
    raise TypeError(
        "Gather op cannot have the index vector dimension as a batching "
        f"dimension; got {start_indices_batching_dims}."
    )

  if len(operand_batching_dims) != len(start_indices_batching_dims):
    raise TypeError(
        "Gather op requires equal numbers of operand_batching_dims and "
        f"start_indices_batching_dims, got {operand_batching_dims} and"
        f"{start_indices_batching_dims}."
    )

  operand_batch_shape = tuple(operand.shape[i] for i in operand_batching_dims)
  indices_batch_shape = tuple(
      indices.shape[i] for i in start_indices_batching_dims
  )
  if not core.definitely_equal_shape(operand_batch_shape, indices_batch_shape):
    raise TypeError(
        "Gather op requires operand batching dimensions and indices batching "
        f"dimensions to have the same shape, got {operand_batch_shape} and "
        f"{indices_batch_shape}."
    )
  # End ValidateGatherDimensions

  if _rank(operand) != len(slice_sizes):
    raise TypeError(f"Gather op must have one slice size for every input "
                    f"dimension; got: len(slice_sizes)={len(slice_sizes)}, "
                    f"input_shape.rank={_rank(operand)}")

  if len(slice_sizes) != len(offset_dims) + len(collapsed_slice_dims) + len(
      operand_batching_dims
  ):
    raise TypeError(
        "All components of the offset index in a gather op must "
        "either be a offset dimension or explicitly collapsed/batching; "
        f"got len(slice_sizes)={len(slice_sizes)}, "
        f"output_slice_sizes={offset_dims}, collapsed_slice_dims="
        f"{collapsed_slice_dims}, operand_batching_dims="
        f"{operand_batching_dims}."
    )

  for i in range(len(slice_sizes)):
    slice_size = slice_sizes[i]
    corresponding_input_size = operand.shape[i]

    if not core.is_empty_shape(indices.shape) and not (
        slice_size >= 0 and corresponding_input_size >= slice_size
    ):
      raise TypeError(f"Slice size at index {i} in gather op is out of range, "
                      f"must be within [0, {corresponding_input_size} + 1), "
                      f"got {slice_size}.")

  for i in range(len(collapsed_slice_dims)):
    bound = slice_sizes[collapsed_slice_dims[i]]
    if bound != 1:
      raise TypeError(f"Gather op can only collapse slice dims with bound 1, "
                      f"but bound is {bound} for index "
                      f"{collapsed_slice_dims[i]} at position {i}.")

  for i in range(len(operand_batching_dims)):
    bound = slice_sizes[operand_batching_dims[i]]
    if bound > 1:
      raise TypeError(f"Gather op can only have operand batching dims with "
                      f"bound 0/1, but bound is {bound} for index "
                      f"{operand_batching_dims[i]} at position {i}."
      )

  return _gather_shape_computation(indices, dimension_numbers, slice_sizes)

