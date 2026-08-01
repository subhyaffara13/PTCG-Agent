
def _create_device_mesh_for_nd_torus(
    physical_mesh: np.ndarray,
    mesh_shape: Sequence[int],
    *,
    allow_split_physical_axes: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
  """Assigns logical parallelism axes to physical axes of an N-D torus network.

  Given logical parallelism axes with sizes in `mesh_shape` and devices in an
  N-dimensional torus network represented by `physical_mesh`, maps each logical
  axis to one or more physical axes. Prefer to map more-performance-sensitive
  logical axes to larger numbers of physical axes to maximize the bandwidth
  available to them. Also prefer to assign logical axes to multiple physical
  axes of the same size (e.g., a 2D square) rather than multiple physical axes
  of different sizes when possible.

  If allow_split_physical_axes = False (default), this routine will error out
  instead of splitting a physical axis over more than one logical axis (which
  would reduce total usable bandwidth).

  Let's use a concrete example to explain the concepts and considerations.

  As an example, suppose the logical mesh is [data, model], for data and model
  parallelism respectively. Also suppose that data parallelism is less
  performance sensitive than model parallelism. Consider a 3D TPU pod slice of
  shape 4x4x16, represented by a physical mesh of shape (4, 4, 16).

  A TPU pod slice has equal bandwidth along all axes with wraparound links, but
  a 2D plane of size 4x4 may have faster XLA collective implementations than a
  non-square plane or a 1D subgroup. If the mesh_shape is [16, 16], we may want
  the more performance sensitive `model` axis to be mapped to the 4x4 XY plane.

  Args:
    physical_mesh: a np.ndarray of devices in the shape of the N-D torus
      physical topology.
    mesh_shape: shape of the logical mesh (size of the various logical
      parallelism axes), with axes ordered by increasing network intensity.
    allow_split_physical_axes: If True, we would split physical axes if
      necessary to fit the desired mesh shape.

  Returns:
    An np.ndarray of devices in the shape of the logical mesh (mesh_shape), with
      each logical parallelism axis mapped to one or more physical mesh axes.
    The axis assignment matrix, which is a 2-d array mapping from
      (physical_axis, logical_axis) to the size assigned, with the invariant
      np.prod(assignment, axis=1) = physical_mesh_shape, and
      np.prod(assignment, axis=0) = mesh_shape.
  """
  # Remaining physical axes to be assigned to logical axes.
  assignable_physical_mesh = list(physical_mesh.shape)
  # Map each logical axis to a subset of physical axes.
  assignment: list[tuple[int, ...]] = [() for _ in mesh_shape]

  # Assign logical axes from highest network intensity to lowest.
  # `mesh_shape` is assumed to ordered by lowest network intensity first, so
  # reverse it first.
  for logical_axis_index, logical_axis_size in reversed(
      list(enumerate(mesh_shape))
  ):
    # Preferentially map to more physical axes first for higher bandwidth.
    for num_axes in range(len(physical_mesh.shape), 0, -1):
      # Try assign to any subset of size num_axes. Generate all candidates.
      indices_and_axes = itertools.combinations(
          enumerate(assignable_physical_mesh), num_axes
      )
      for elem in indices_and_axes:
        c_indices, c_axes = zip(*elem)
        # TODO(zhangqiaorjc): Due to limitations in XLA, 2D collectives only
        # implemented for square 2D plane. Mapping a physical axis to two
        # logical axes might be slower for non-square 2D plane, e.g., map 32 to
        # 4x8 or a single axis. If XLA 2D collectives support non-square plane
        # soon, we can continue to preferentially map to 2D plane in general,
        # otherwise, we should treat non-square 2D plane and 1D submesh equally.
        if np.prod(c_axes) == logical_axis_size:
          assignment[logical_axis_index] = c_indices
          # Zero the assigned physical axes.
          assignable_physical_mesh = [
              0 if i in c_indices else v
              for i, v in enumerate(assignable_physical_mesh)
          ]
          break
      if assignment[logical_axis_index]:
        # We already found an assignment from one candidate above.
        break
    else:
      # If the num_axes for loop did not break, i.e. none of the candidates work
      # goto here with this while-else construct.
      if logical_axis_size > 1:
        if not allow_split_physical_axes:
          # Although this is now implemented, there are downstream tasks
          # counting on this being a NotImplementedError.
          raise NotImplementedError(
              'Failed to find assignment for logical_axis_index'
              f' {logical_axis_index} of size {logical_axis_size} with'
              f' remaining assignable mesh {assignable_physical_mesh}. The size'
              ' of each axis in your logical mesh must be equal to the product'
              ' of some subset of the physical mesh axis sizes. E.g. logical'
              ' mesh (4, 16) is compatible with physical mesh 4x4x4 since 4=4'
              ' and 16=4x4. If you want to split physical axes, set '
              ' allow_split_physical_axes to True.'
          )
        else:
          # We will try finding an assignment, even if that means splitting the
          # physical axes, which requires a more sophisticated implementation.
          return _create_device_mesh_for_nd_torus_splitting_axes(
              physical_mesh, mesh_shape
          )

  # Flatten the assignment, e.g., [(), (2,), (0, 1)] -> (2, 0, 1).
  transpose: list[int] = []
  assignment_array = np.ones(
      [len(physical_mesh.shape), len(mesh_shape)], dtype=np.int64
  )
  for i, x in enumerate(assignment):
    for y in x:
      physical_mesh_axis = int(y)
      assignment_array[physical_mesh_axis, i] = physical_mesh.shape[
          physical_mesh_axis
      ]
      transpose.append(physical_mesh_axis)
  return (
      physical_mesh.transpose(transpose).reshape(mesh_shape),
      assignment_array,
  )

