
def get_ctx_mesh(use_resource_env):
  if use_resource_env:
    return mesh_lib.thread_resources.env.physical_mesh
  else:
    conc_mesh = mesh_lib.get_concrete_mesh()
    if not conc_mesh.empty:
      return conc_mesh
    else:
      abs_mesh = mesh_lib.get_abstract_mesh()
      # TODO(yashkatariya): Make top-level use_abstract_mesh work with Auto mode
      # too. But there are failures in user code so restricting it to Explicit
      # mode for now.
      if not abs_mesh.empty and abs_mesh._any_axis_explicit:
        return abs_mesh
      return conc_mesh

