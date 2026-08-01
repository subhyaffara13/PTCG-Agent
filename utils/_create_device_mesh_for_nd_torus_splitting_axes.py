
def _create_device_mesh_for_nd_torus_splitting_axes(
    physical_mesh: np.ndarray,
    mesh_shape: Sequence[int],
) -> tuple[np.ndarray, np.ndarray]:
  """Assigns logical parallelism axes to physical axes of an N-D torus network.

  This implementation allows creating meshes that requires splitting physical
  axes, and thus one could produce logical mesh of any shape, as long as the
  number of devices matches, e.g.,

  - Creating 2x2x4 from 4x4;

  - Creating 2x2x16 from 8x8;

  Args:
    physical_mesh: a np.ndarray of devices in the shape of the N-D torus
      physical topology.
    mesh_shape: shape of the logical mesh (size of the various logical
      parallelism axes), with axes ordered by increasing network intensity.

  Returns:
    An np.ndarray of devices in the shape of the logical mesh (mesh_shape), with
      each logical parallelism axis mapped to one or more physical mesh axes.
    The axis assignment matrix, which is a 2-d array mapping from
      (physical_axis, logical_axis) to the size assigned, with the invariant
      np.prod(assignment, axis=1) = physical_mesh_shape, and
      np.prod(assignment, axis=0) = mesh_shape.
  """
  if np.prod(physical_mesh.shape) != np.prod(mesh_shape):
    raise ValueError(
        'The number of devices in physical mesh'
        f' {physical_mesh.shape} does not match the number of devices'
        f' in logical mesh {mesh_shape}.'
    )

  physical_mesh_shape = physical_mesh.shape
  logical_mesh_shape = tuple(mesh_shape)

  # (Partial) assignment map as an 2-d array [p_axis, l_axis] -> size.
  assignment = np.ones(
      [len(physical_mesh_shape), len(logical_mesh_shape)], dtype=np.int64
  )

  # Process logical axes from highest network intensity to lowest.
  # `mesh_shape` is assumed to ordered by lowest network intensity first, so
  # reverse it.
  for logical_axis, logical_axis_size in reversed(
      list(enumerate(logical_mesh_shape))
  ):
    # Go over all the possible assignment for the logical axis, including the
    # one that splits multiple physical axes.
    best_logical_axis_assignment: np.ndarray | None = None
    for logical_axis_assignment in _enumerate_feasible_logical_axis_assignments(
        physical_mesh_shape, assignment, logical_axis_size
    ):
      # TODO(rosun): Instead of using heuristics, replace this with a proper
      # scoring function reflecting the underlying hardware properties.
      if (
          best_logical_axis_assignment is None
          or _prefer_first_logical_axis_assignment(
              logical_axis_assignment,
              best_logical_axis_assignment,
              physical_mesh_shape=physical_mesh_shape,
              assignment=assignment,
          )
      ):
        best_logical_axis_assignment = logical_axis_assignment
    assignment[:, logical_axis] = best_logical_axis_assignment  # pyrefly: ignore[unsupported-operation]  # numpy 2.2

  # Read out the assignment.
  logical_mesh = _generate_logical_mesh(
      physical_mesh, logical_mesh_shape, assignment
  )

  return logical_mesh, assignment

