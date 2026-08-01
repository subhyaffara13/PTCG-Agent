
def _prefer_first_logical_axis_assignment(
    x: np.ndarray,
    y: np.ndarray,
    *,
    physical_mesh_shape: Sequence[int],
    assignment: np.ndarray,
) -> bool:
  """Returns True if the first axis assignment is preferred over the second.

  For now, this is implemented with some very simple heuristics. However,
  it is possible to introduce e.g., a value function here based on a more
  precise model of the underlying hardware.

  TODO(rosun): Use a proxy of network capacity to select the partitions.

  Args:
    x: Logical axis assignment as [len(physical_mesh_shape)] array.
    y: Logical axis assignment as [len(physical_mesh_shape)] array.
    physical_mesh_shape: Physical mesh shape.
    assignment: Assignment matrix.

  Returns:
    True if x is preferred over y.
  """
  # Prefer occupying complete physical axes. I don't have a good reason for
  # this, except that it is compatible with the existing behavior.
  #
  # E.g., on 4 x 4 x 8, [4, 4, -] will be preferred over [4, -, 4], and then
  # over [2, 2, 4].
  x_whole_axis_size = np.prod(
      [s for i, s in enumerate(x) if s == physical_mesh_shape[i]]
  )
  y_whole_axis_size = np.prod(
      [s for i, s in enumerate(y) if s == physical_mesh_shape[i]]
  )

  if x_whole_axis_size != y_whole_axis_size:
    return x_whole_axis_size > y_whole_axis_size

  # Prefer occupying more whole physical axes for better bandwidth.
  #
  # This is consistent with existing logic, i.e., 2 x 2 is preferred over 4.
  x_num_whole_axes = len(
      [1 for i, s in enumerate(x) if s == physical_mesh_shape[i] and s > 1]
  )
  y_num_whole_axes = len(
      [1 for i, s in enumerate(y) if s == physical_mesh_shape[i] and s > 1]
  )

  if x_num_whole_axes != y_num_whole_axes:
    return x_num_whole_axes > y_num_whole_axes

  # Prefer taking physical axes that are not taken by logical axes of higher
  # network intensity. E.g., for a 4 x 4 x 4, suppose that the previous
  # assignments are 1 x 2 x 4, and we want to place a new logical axis of size
  # 2, we will go for [2, 1, 1] instead of [1, 2, 1], as the latter choice will
  # tap into bandwidth already taken by the higher intensity axis.
  assigned_physical_mesh_shape = np.prod(assignment, axis=-1)

  x_non_overlapping_axis_size = np.prod(
      [s for i, s in enumerate(x) if assigned_physical_mesh_shape[i] > 1]
  )
  y_non_overlapping_axis_size = np.prod(
      [s for i, s in enumerate(y) if assigned_physical_mesh_shape[i] > 1]
  )

  if x_non_overlapping_axis_size != y_non_overlapping_axis_size:
    return x_non_overlapping_axis_size > y_non_overlapping_axis_size

  # Otherwise sort by reverse lexical graphical order, to be consistent with
  # existing behavior.
  return tuple(x) > tuple(y)

