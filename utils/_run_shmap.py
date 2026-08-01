
def _run_shmap(f, mesh, manual_axes, args, mats, check_vma):
  assert not mesh.manual_axes
  trace = ShardMapTrace(mesh, manual_axes, check_vma)
  in_tracers = map(partial(ShardMapTracer, trace), mats, args)
  inner_mesh = _as_manual_mesh(mesh, manual_axes)
  with (core.set_current_trace(trace), _extend_axis_env(mesh, manual_axes),
        use_abstract_mesh(inner_mesh), config._check_vma(check_vma)):
    ans, out_specs = f(*in_tracers).unpack_aux()
    outs, outs_mat = ans.map(trace.to_val_mat_pair).unzip2()
  return outs, out_specs, list(outs_mat)

