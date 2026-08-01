
def _process_in_axis_resources(in_shardings_treedef, in_shardings_leaves,
                               in_layouts_treedef, in_layouts_leaves,
                               in_avals, dbg: core.DebugInfo,
                               device_or_backend_set, kws):
  if kws:
    in_tree = in_avals.tree_without_statics
  else:
    in_tree, _ = treedef_children(in_avals.tree_without_statics)

  orig_in_shardings = tree_unflatten(in_shardings_treedef, in_shardings_leaves)
  # Only do this if original in_shardings are unspecified.
  if isinstance(orig_in_shardings, UnspecifiedValue):
    in_shardings_flat = (orig_in_shardings,) * len(in_avals)
  else:
    in_shardings_flat = flatten_axis_resources(
        "pjit in_shardings", in_tree, orig_in_shardings, tupled_args=True)

  in_layouts = tree_unflatten(in_layouts_treedef, in_layouts_leaves)
  if in_layouts is None:
    in_layouts_flat = (in_layouts,) * len(in_avals)
  else:
    in_layouts_flat = flatten_axis_resources(
        "pjit in_layouts", in_tree, in_layouts, tupled_args=True)

  pjit_check_aval_sharding(in_shardings_flat, in_avals,
                           dbg.safe_arg_names(len(in_avals)),
                           "pjit arguments", allow_uneven_sharding=False)
  check_aval_layout_compatibility(
      in_layouts_flat, in_avals,
      dbg.safe_arg_names(len(in_avals)), "jit arguments")
  return in_shardings_flat, in_layouts_flat

