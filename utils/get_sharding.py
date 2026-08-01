
def get_sharding(sharding, shape):
  """Modifies and checks the sharding.

  Some modifications/checks include:
    * Making the length of specs the same as ndim
    * If a mesh axis is mentioned in pspec is Auto/Manual, replace it with None
    * Checking for len(spec)-ndim match
    * Checking if the mesh is an AbstractMesh.
  """
  ndim = len(shape)
  if sharding is None:
    return _empty_sharding(ndim)

  out_s = _maybe_modify_sharding(sharding, ndim)
  if len(out_s.spec) != ndim:
    raise ValueError(
        "Length of sharding.spec must be equal to aval's ndim. Got"
        f" sharding.spec {out_s.spec}, aval.ndim {ndim} and sharding {out_s}")
  if not isinstance(out_s.mesh, mesh_lib.AbstractMesh):
    raise ValueError("Mesh of an aval must be an AbstractMesh. "
                     f"Got {out_s.mesh} of type {type(out_s.mesh)}")
  _check_divisibility(out_s, shape)
  if out_s.memory_kind is not None:
    raise ValueError(
        "sharding with memory_kind is not allowed. Please use `jax.device_put`"
        f" to transfer to different memory spaces. Got {sharding=}")
  return out_s


def get_sharding(tree: Any, mesh: jax.sharding.Mesh) -> Any:
  """Extracts a jax.sharding tree from a PyTree containing ``Partitioned`` values and a mesh."""
  def f(x: Any) -> jax.sharding.Sharding | None:
    if hasattr(x, 'get_sharding'):
      return x.get_sharding(mesh)
    pspec = _get_leaf_pspec(x)
    if pspec is None:
      return None
    return jax.sharding.NamedSharding(mesh, pspec)

  return jax.tree_util.tree_map(
      f, tree, is_leaf=lambda x: isinstance(x, AxisMetadata)
  )

