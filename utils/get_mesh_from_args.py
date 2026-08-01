
def get_mesh_from_args(args_flat, mesh):
  for a in args_flat:
    if (hasattr(a, 'sharding') and isinstance(a.sharding, NamedSharding)
        and not a.sharding.mesh.is_scalar):  # pyrefly: ignore[missing-attribute]

      if a.sharding.mesh.shape_tuple != mesh.shape_tuple:
        aval = core.shaped_abstractify(a)
        raise ValueError(
            f"Mesh shape of the input {a.sharding.mesh.shape_tuple} does not"
            " match the mesh shape passed to shard_map "
            f" {mesh.shape_tuple} for shape {aval.str_short()}")
      mesh = a.sharding.mesh
  if isinstance(mesh, AbstractMesh):
    raise ValueError(
        "Please pass `jax.Array`s with a `NamedSharding` as input to"
        " `shard_map` when passing `AbstractMesh` to the mesh argument.")
  assert isinstance(mesh, Mesh)
  return mesh

