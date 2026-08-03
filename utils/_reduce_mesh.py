from typing import Any, Callable

def _reduce_mesh(
    mesh: jax.sharding.Mesh,
) -> tuple[Callable[..., jax.sharding.Mesh], Any]:
  mesh_device_ids = np.vectorize(lambda d: d.id, otypes=[int])(mesh.devices)
  return _unreduce_mesh, (mesh_device_ids, mesh.axis_names, mesh.axis_types)

