
def _scatter_shape_rule(operand, indices, updates, *, update_jaxpr,
                        update_consts, dimension_numbers, indices_are_sorted,
                        unique_indices, mode):
  """Validates the well-formedness of the ``dimension_numbers`` argument to
  Scatter.

  The code implements the checks based on the detailed operation semantics of
  XLA's `Scatter <https://www.openxla.org/xla/operation_semantics#scatter>`_
  operator and following the outline of the implementation of
  ShapeInference::InferScatterShape in TensorFlow.
  """

  update_window_dims = dimension_numbers.update_window_dims
  inserted_window_dims = dimension_numbers.inserted_window_dims
  operand_batching_dims = dimension_numbers.operand_batching_dims
  scatter_indices_batching_dims = dimension_numbers.scatter_indices_batching_dims
  scatter_dims_to_operand_dims = dimension_numbers.scatter_dims_to_operand_dims
  # Note: in JAX, index_vector_dim is always computed as below, cf. the
  # documentation of the ScatterDimensionNumbers class.
  index_vector_dim = _rank(indices) - 1

  # This case should never happen in JAX, due to the implicit construction of
  # index_vector_dim, but is included for completeness.
  if _rank(indices) < index_vector_dim or index_vector_dim < 0:
    raise TypeError(f"Scatter index leaf dimension must be within [0, "
                    f"rank(indices) + 1). rank(indices) is {_rank(indices)} "
                    f"and scatter index leaf dimension is {index_vector_dim}.")

  expanded_indices_shape = list(indices.shape)
  # This case should never happen in JAX, due to the implicit construction of
  # index_vector_dim, but is included for completeness.
  if len(expanded_indices_shape) == index_vector_dim:
    expanded_indices_shape.append(1)

  expected_updates_rank = (len(expanded_indices_shape) - 1 +
                           len(update_window_dims))

  if _rank(updates) != expected_updates_rank:
    raise TypeError(f"Updates tensor must be of rank {expected_updates_rank}; "
                    f"got {_rank(updates)}.")

  # Validate update_window_dims
  _is_sorted(update_window_dims, "scatter", "update_window_dims")
  _no_duplicate_dims(update_window_dims, "scatter", "update_window_dims")
  _sorted_dims_in_range(update_window_dims, _rank(updates), "scatter",
                        "update_window_dims")

  # Validate inserted_window_dims
  _is_sorted(inserted_window_dims, "scatter", "inserted_window_dims")
  _no_duplicate_dims(inserted_window_dims, "scatter", "inserted_window_dims")
  _sorted_dims_in_range(inserted_window_dims, _rank(operand), "scatter",
                        "inserted_window_dims")

  # Validate operand_batching_dims and scatter_indices_batching_dims
  _is_sorted(operand_batching_dims, "scatter", "operand_batching_dims")
  _no_duplicate_dims(operand_batching_dims, "scatter", "operand_batching_dims")
  _sorted_dims_in_range(
      operand_batching_dims, _rank(operand), "scatter", "operand_batching_dims"
  )
  _disjoint_dims(inserted_window_dims, operand_batching_dims, "scatter",
                 "inserted_window_dims", "operand_batching_dims")
  _disjoint_dims(scatter_dims_to_operand_dims, operand_batching_dims, "scatter",
                 "scatter_dims_to_operand_dims", "operand_batching_dims")

  _no_duplicate_dims(
      scatter_indices_batching_dims, "scatter", "scatter_indices_batching_dims"
  )
  _dims_in_range(
      scatter_indices_batching_dims,
      _rank(indices),
      "scatter",
      "scatter_indices_batching_dims",
  )
  if index_vector_dim in scatter_indices_batching_dims:
    raise TypeError(
        "Scatter op cannot have the index vector dimension as a batching "
        f"dimension; got {scatter_indices_batching_dims}.")

  if len(operand_batching_dims) != len(scatter_indices_batching_dims):
    raise TypeError(
        "Scatter op requires equal numbers of operand_batching_dims and "
        f"scatter_indices_batching_dims, got {operand_batching_dims} and "
        f"{scatter_indices_batching_dims}."
    )

  operand_batch_shape = tuple(operand.shape[i] for i in operand_batching_dims)
  indices_batch_shape = tuple(
      indices.shape[i] for i in scatter_indices_batching_dims
  )
  if not core.definitely_equal_shape(operand_batch_shape, indices_batch_shape):
    raise TypeError(
        "Scatter op requires operand batching dimensions and indices batching "
        f"dimensions to have the same shape, got {operand_batch_shape} and "
        f"{indices_batch_shape}."
    )
  updates_batching_dims = _get_updates_batching_dims(
      scatter_indices_batching_dims, update_window_dims, index_vector_dim,
      updates.shape)
  updates_batch_shape = tuple(updates.shape[i] for i in updates_batching_dims)
  if not core.definitely_equal_shape(operand_batch_shape, updates_batch_shape):
    raise TypeError(
        "Scatter op requires operand batching dimensions and updates batching "
        f"dimensions to have the same shape, got {operand_batch_shape} and "
        f"{updates_batch_shape}."
    )
  # Validate window_size
  window_size = (
      len(update_window_dims) +
      len(inserted_window_dims) +
      len(operand_batching_dims)
  )
  if _rank(operand) != window_size:
    raise TypeError(f"Scatter op has window of size {window_size}; doesn't "
                    f"match operand of rank {_rank(operand)}.")

  # Validate scatter_dims_to_operand_dims
  if (len(scatter_dims_to_operand_dims) !=
      indices.shape[index_vector_dim]):
    raise TypeError(f"Scatter op has {len(scatter_dims_to_operand_dims)} "
                    f"elements in scatter_dims_to_operand_dims and the bound "
                    f"of dimension {index_vector_dim=} of "
                    f"indices is {indices.shape[index_vector_dim]}. These two "
                    f"numbers must be equal")

  for i in range(len(scatter_dims_to_operand_dims)):
    dim = scatter_dims_to_operand_dims[i]
    if dim < 0 or dim >= _rank(operand):
      raise TypeError(f"Invalid scatter_dims_to_operand_dims mapping; domain "
                      f"is [0, {_rank(operand)}), got: {i}->{dim}.")

  _no_duplicate_dims(scatter_dims_to_operand_dims, "scatter",
                     "scatter_dims_to_operand_dims")

  max_update_slice_sizes = [
      operand.shape[i]
      for i in range(len(operand.shape))
      if (
          i not in set(inserted_window_dims)
          and i not in set(operand_batching_dims)
      )
  ]

  for i in range(len(update_window_dims)):
    update_window_dim = update_window_dims[i]
    if max_update_slice_sizes[i] < updates.shape[update_window_dim]:
      raise TypeError(f"Bounds of the window dimensions of updates must not "
                      f"exceed the bounds of the corresponding dimensions of "
                      f"operand. For dimension {update_window_dim}, updates "
                      f"bound is {updates.shape[update_window_dim]}, operand "
                      f"bound is {max_update_slice_sizes[i]}.")

  update_scatter_dims = [dim for dim in range(_rank(updates)) if dim not in
                         set(update_window_dims)]

  scatter_dims_seen = 0
  for i in update_scatter_dims:
    if scatter_dims_seen == index_vector_dim:
      scatter_dims_seen += 1
    if not core.definitely_equal(updates.shape[i], expanded_indices_shape[scatter_dims_seen]):
      raise TypeError(f"Bounds of the scatter dimensions of updates must be "
                      f"the same as the bounds of the corresponding dimensions "
                      f"of scatter indices. For scatter dimension {i}, updates "
                      f"bound is {updates.shape[i]}, indices bound is "
                      f"{expanded_indices_shape[scatter_dims_seen]}.")
    scatter_dims_seen += 1

  return operand.shape

