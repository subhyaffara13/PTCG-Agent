
def _get_mesh_shape_and_semantics(
    mesh: pallas_core.Mesh,
) -> tuple[tuple[tuple[jax_core.AxisName, int], ...], tuple[str, ...]]:
  match mesh:
    case (
        tpu_core.TensorCoreMesh()
        | sc_core.ScalarSubcoreMesh()
        | sc_core.VectorSubcoreMesh()
    ):
      if isinstance(mesh, tpu_core.TensorCoreMesh) and len(mesh.shape) > 1:
        raise NotImplementedError(
            "TensorCoreMesh with more than one dimension is not supported."
        )
      dimension_semantics = tuple(
          _canonicalize_dimension_semantic(s) for s in mesh.dimension_semantics
      )
      mesh_shape = tuple(mesh.shape.items())
    case _:
      # Do some duck-typing to get the mesh shape and dimension semantics.
      if hasattr(mesh, "shape") and hasattr(mesh, "dimension_semantics"):
        dimension_semantics = tuple(
            _canonicalize_dimension_semantic(s)
            for s in mesh.dimension_semantics
        )
        mesh_shape = tuple(mesh.shape.items())
      else:
        raise ValueError(f"Unsupported mesh type: {mesh}")
  return mesh_shape, dimension_semantics

