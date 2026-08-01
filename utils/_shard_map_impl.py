
def _shard_map_impl(trace, prim, fun, args, *, mesh, in_specs,
                    check_vma, newly_manual_axes, debug_info):
  del prim
  if isinstance(mesh, AbstractMesh):
    concrete_mesh = get_concrete_mesh()
    mesh = concrete_mesh if not concrete_mesh.empty else mesh
    mesh = get_mesh_from_args(args, mesh)
  cur_mesh = get_abstract_mesh()
  args_ = map(partial(_unmatch_spec, mesh, check_vma, cur_mesh, newly_manual_axes),
              in_specs, args)
  in_mat = map(_spec_to_mat, in_specs)
  outs, out_specs, out_mat = _run_shmap(fun, mesh, newly_manual_axes, args_,
                                        in_mat, check_vma)
  out_avals = outs.map(lambda x: core.mapped_aval(x.shape[0], 0, core.typeof(x)))
  _check_names(out_specs, out_avals)
  if check_vma:
    _check_mats(mesh, out_specs, out_avals)
    src_pspecs = tuple(_mat_to_spec(mesh, m) for m in out_mat)
  else:
    src_pspecs = tuple(P(order_wrt_mesh(mesh, newly_manual_axes))
                       for _ in range(len(out_mat)))
  dst_pspecs = out_specs
  return outs.map3(partial(_match_spec, mesh, check_vma, newly_manual_axes),
                   src_pspecs, dst_pspecs)

