
def _get_out_shardings(out_tree, pspecs, out_shardings_thunk):
  """Get flattened output shardings, combining pspec flattening and sharding lookup."""
  out_pspecs_flat = pjit_lib.flatten_axis_resources(
      "output pspecs", out_tree, pspecs, tupled_args=True
  )
  return tuple(zip(*[out_shardings_thunk(p) for p in out_pspecs_flat]))

