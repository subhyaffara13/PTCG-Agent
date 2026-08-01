
def _flatten_pspecs(name, in_tree, pspecs_thunk):
  return pjit_lib.flatten_axis_resources(
      name, in_tree, pspecs_thunk(), tupled_args=True)

