
def _run_shmap_lu(f, mesh, manual_axes, args, mats, check_vma):
  assert not mesh.manual_axes
  trace = ShardMapTrace(mesh, manual_axes, check_vma)
  in_tracers = map(partial(ShardMapTracer, trace), mats, args)
  inner_mesh = _as_manual_mesh(mesh, manual_axes)
  with (core.set_current_trace(trace), _extend_axis_env(mesh, manual_axes),
        use_abstract_mesh(inner_mesh), config._check_vma(check_vma)):
    ans = f.call_wrapped(*in_tracers)
    outs, out_mat = unzip2(map(trace.to_val_mat_pair, ans))
  return outs, out_mat

