
def check_avals_context_mesh(avals, prim_name):
  cur_mesh = mesh_lib.get_abstract_mesh()
  for a in avals:
    # TODO(yashkatariya): Should be cur_mesh.unset
    if cur_mesh.empty or a.sharding.mesh.empty:
      continue
    # avals can have meshes with different axis_names so allow that in
    # full auto mode.
    if a.sharding.mesh.are_all_axes_auto and cur_mesh.are_all_axes_auto:
      continue
    if a.sharding.mesh != cur_mesh:
      raise ValueError(
          f"For primitive {prim_name}, context mesh {cur_mesh} should match"
          f" the aval mesh {a.sharding.mesh} for shape {a.str_short()}. This"
          " error occurs at source: "
          f" {source_info_util.summarize(source_info_util.current())}")
    if not isinstance(a.memory_space, MemorySpace):
      raise TypeError(
          f"Primitive {prim_name} got aval {a} with unknown memory_space type:"
          f" {type(a.memory_space)}")

