
def _generate_logical_mesh(
    physical_mesh: np.ndarray,
    logical_mesh_shape: Sequence[int],
    assignment: np.ndarray,
) -> np.ndarray:
  """Compute the logical mesh from assignment map.

  Args:
    physical_mesh: Physical device mesh.
    logical_mesh_shape: Logical mesh shape.
    assignment: 2-d assignment matrix shape [physical_dims, logical_dims].

  Returns:
    Logical mesh reshaped from physical mesh.
  """
  physical_indices = np.broadcast_to(
      np.expand_dims(
          np.arange(len(physical_mesh.shape), dtype=np.int64), axis=-1
      ),
      assignment.shape,
  ).reshape([-1])

  logical_indices = np.broadcast_to(
      np.expand_dims(
          np.arange(len(logical_mesh_shape), dtype=np.int64), axis=0
      ),
      assignment.shape,
  ).reshape([-1])

  # Axes of logical mesh is ordered by (physical_axis, logical_axis).
  #
  # Note that we sort for each physical_axis the logical_axis, so that higher
  # intensity logical axes are replicated at inner (minor) dimensions.
  #
  # E.g., if a dimension size is 12 = 3x4, where 3 is higher intensity and 4
  # is lower, we want to reshape so that it becomes 12 = 4x3. Imagine in the
  # 1-d case, this will allow more connections between the higher intensity
  # axes.
  logical_mesh = np.reshape(physical_mesh, assignment.reshape([-1]))

  # We will then group by l_axis as this is what is expected from output.
  _, _, transpose_axes = zip(
      *sorted(
          zip(logical_indices, physical_indices, range(len(logical_indices)))
      )
  )
  logical_mesh = np.transpose(logical_mesh, transpose_axes)

  # Reshape to add the trivial dimensions back.
  logical_mesh = np.reshape(logical_mesh, logical_mesh_shape)

  return logical_mesh

