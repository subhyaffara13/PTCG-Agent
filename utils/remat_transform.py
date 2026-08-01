
def remat_transform(policy, f, *args):
  dbg = api_util.debug_info("remat", f, args, {})
  with core.take_current_trace() as parent_trace:
    jaxpr_trace = pe.DynamicJaxprTrace(None)
    trace = RematTrace(parent_trace, jaxpr_trace, core.TraceTag(), policy)
    args_ft = FlatTree.flatten_static_argnums_argnames(args, {}, (), ())
    in_tracers = args_ft.map(
        lambda x: RematTracer(trace, x, jaxpr_trace.new_arg(typeof(x), None)))  # type: ignore # noqa F821
    with core.set_current_trace(trace):
      args, kwargs = in_tracers.unflatten()
      ans_pytree = f(*args, **kwargs)
      dbg = dbg.set_result_paths(ans_pytree)
      ans_ft = FlatTree.flatten(ans_pytree)
      del ans_pytree, args, kwargs
    out_ft, out_tracer_ft = ans_ft.map(trace.to_val_tracer_pair).unzip2()
    src = source_info_util.current()
    out_tracer_ft = out_tracer_ft.map(partial(jaxpr_trace.to_jaxpr_tracer, source_info=src))
    jaxpr, res = jaxpr_trace.to_jaxpr(list(out_tracer_ft), dbg, src)
    in_tree, out_tree = args_ft.tree, out_ft.tree
    del trace, in_tracers, out_tracer_ft
  def f_rem(res, *args):
    args_flat = tree_leaves_checked(in_tree, (args, {}))
    out_flat = core.eval_jaxpr(jaxpr, res, *args_flat)
    return tree_unflatten(out_tree, out_flat)
  return out_ft.unflatten(), Partial(f_rem, map(reduce_precision, res))

