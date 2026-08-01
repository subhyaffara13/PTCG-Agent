
def _check_and_canonicalize_out_shardings(
    out_shardings_treedef, out_shardings_leaves, out_layouts_treedef,
    out_layouts_leaves, out_tree, out_avals,
    debug_info: core.DebugInfo,
    device_or_backend_set):
  orig_out_shardings = tree_unflatten(out_shardings_treedef, out_shardings_leaves)
  if isinstance(orig_out_shardings, (UnspecifiedValue, Sharding)):
    out_shardings_flat = (orig_out_shardings,) * len(out_avals)
  else:
    out_shardings_flat = flatten_axis_resources(
        "pjit out_shardings", out_tree, orig_out_shardings,
        tupled_args=False)

  out_layouts = tree_unflatten(out_layouts_treedef, out_layouts_leaves)
  if out_layouts is None:
    out_layouts_flat = (out_layouts,) * len(out_avals)
  else:
    out_layouts_flat = flatten_axis_resources(
        "pjit out_layouts", out_tree, out_layouts, tupled_args=False)

  pjit_check_aval_sharding(
      out_shardings_flat, out_avals,
      debug_info.safe_result_paths(len(out_avals)),
      "pjit outputs", allow_uneven_sharding=False)
  check_aval_layout_compatibility(
      out_layouts_flat, out_avals,
      debug_info.safe_result_paths(len(out_avals)),
      "jit outputs")
  return out_shardings_flat, out_layouts_flat

