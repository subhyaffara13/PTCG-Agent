
def _shmap_checks(mesh, axis_names, in_specs, out_specs, _smap):
  if mesh is None:
    mesh = get_abstract_mesh()
    if mesh.empty:
      raise ValueError(
          "The context mesh cannot be empty. Use"
          " `jax.set_mesh(mesh)` to enter into a mesh context")
  else:
    ctx_mesh = get_abstract_mesh()
    if not ctx_mesh.empty and mesh.abstract_mesh != ctx_mesh:
      raise ValueError(
          f"The context mesh {ctx_mesh} should match the mesh passed to"
          f" shard_map {mesh}")

  if not isinstance(mesh, (Mesh, AbstractMesh)):
    raise TypeError("shard_map requires a `jax.sharding.Mesh` or a "
                    "`jax.sharding.AbstractMesh` instance for its "
                    f"second argument, but got {mesh} of type {type(mesh)}.")
  if mesh.empty:
    raise ValueError(f"shard_map requires a non-empty mesh. Got {mesh}")

  mesh_axis_names_wo_vmap = (
      frozenset(mesh.axis_names) - core.get_axis_env().explicit_mesh_axis_names
  )

  if not isinstance(axis_names, (frozenset, set)):
    raise TypeError(
        "`axis_names` argument of shard_map should be of type `frozenset` or"
        f" `set`. Got type: {type(axis_names)}")
  if isinstance(axis_names, set):
    axis_names = frozenset(axis_names)
  if not axis_names:
    axis_names = mesh_axis_names_wo_vmap
  if not axis_names.issubset(mesh_axis_names_wo_vmap):
    raise ValueError(
        f"jax.shard_map requires axis_names={axis_names} to be a subset of "
        f"mesh.axis_names={mesh_axis_names_wo_vmap}")

  if (in_specs is Infer and
      not all(mesh._name_to_type[a] == AxisType.Explicit for a in axis_names)):
    axis_types = ', '.join(str(mesh._name_to_type[a]) for a in axis_names)
    if _smap:
      msg = (f"in_axes was not specified when axis_name={axis_names} was of"
             f" type {axis_types}")
    else:
      msg = ("shard_map in_specs argument must be a pytree of"
             " `jax.sharding.PartitionSpec` instances, but it was `None` when"
             f" {axis_names=} are of type {axis_types}")
    raise TypeError(msg)

  if in_specs is not Infer and in_specs is not None:
    _check_specs(SpecErrorType.input, in_specs, axis_names)
    _check_unreduced(SpecErrorType.input, mesh, axis_names, in_specs)
  _check_specs(SpecErrorType.out, out_specs, axis_names)
  _check_unreduced(SpecErrorType.out, mesh, axis_names, out_specs)
  return mesh, axis_names

