
def canonicalize_sharding(sharding: NamedSharding | PartitionSpec | None,
                          api_name: str, check_mesh_consistency: bool = True
                          ) -> NamedSharding | None:
  if sharding is None:
    return None
  if isinstance(sharding, NamedSharding) and sharding.mesh.empty:
    return None
  if not isinstance(sharding, (NamedSharding, PartitionSpec)):
    raise TypeError(
        f"`out_sharding` argument of {api_name} only supports instances of"
        f" `NamedSharding` or `PartitionSpec`. Got {sharding} of type:"
        f" {type(sharding)}")

  cur_mesh = get_abstract_mesh()
  if isinstance(sharding, PartitionSpec):
    if cur_mesh.empty:
      raise ValueError(
          'Using PartitionSpec when you are not under a mesh context is not'
          ' allowed. Please pass a NamedSharding instance or enter into a mesh'
          f' context via `jax.set_mesh`. Got {sharding}')
    sharding = NamedSharding(cur_mesh, sharding)
  else:
    # There are cases when you have multiple meshes set. Allow that for full
    # auto mode because of existing use cases.
    # TODO(yashkatariya): Remove this once we disallow different meshes and
    # fix the existing use cases.
    if (sharding.mesh.abstract_mesh.are_all_axes_auto and
        cur_mesh.are_all_axes_auto):
      check_mesh_consistency = False
    if (check_mesh_consistency and not cur_mesh.empty and
        sharding.mesh.abstract_mesh != cur_mesh):
      raise ValueError(
          f'Context mesh {cur_mesh} should match the mesh of sharding'
          f' {sharding.mesh.abstract_mesh} passed to {api_name}.'
          ' This error occurs at source: '
          f' {source_info_util.summarize(source_info_util.current())}')
    # TODO(yashkatariya): Maybe allow concrete mesh at the top level
    # i.e `core.trace_state_clean()` for APIs like jnp.zeros, etc?
    if isinstance(sharding.mesh, Mesh):
      sharding = NamedSharding(sharding.mesh.abstract_mesh, sharding.spec)

  for s in it.chain(flatten_spec(sharding.spec), sharding.spec.unreduced,
                    sharding.spec.reduced):
    if s is None:
      continue
    if sharding.mesh._name_to_type[s] in {
        AxisType.Auto, AxisType.Manual}:
      raise ValueError(
          f'PartitionSpec passed to {api_name} cannot contain axis'
          ' names that are of type Auto or Manual. Got PartitionSpec:'
          f' {sharding.spec} with axis name: {s} of type:'
          f' {sharding.mesh._name_to_type[s]}. This error occurs at source: '
          f' {source_info_util.summarize(source_info_util.current())}')
  return sharding

