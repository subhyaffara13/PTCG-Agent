
def _initialize_error_code_ref() -> None:
  """Initialize the error code ref in the current thread.

  The shape and size of the error code array depend on the mesh in the context.
  In single-device environments, the array is a scalar. In multi-device
  environments, its shape and size match those of the mesh.
  """
  # Get mesh from the context.
  mesh = mesh_lib.get_concrete_mesh()

  if mesh.empty:  # single-device case.
    error_code: ArrayLike = np.uint32(_NO_ERROR)

  else:  # multi-device case.
    sharding = NamedSharding(mesh, P(*mesh.axis_names))
    error_code = lax.full(
        mesh.axis_sizes,
        np.uint32(_NO_ERROR),
        sharding=sharding,
    )

  _error_storage.ref = core.new_ref(error_code)

