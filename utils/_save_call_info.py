
def _save_call_info(counter, tracer_args, f, node_stats, compute_flops, compute_vjp_flops, seen):
  "Wrap a function to save its arguments"

  # Used when computing vjp flops
  def do_vjp(*args, **kwargs):
    primals, f_vjp = jax.vjp(f, *args, **kwargs)
    return f_vjp(primals)

  method_name = f.__name__

  @functools.partial(jax.jit)
  def jit_f(graphdef, state):
    args, kwargs = nnx.merge(graphdef, state)
    return f(*args, **kwargs)

  @wraps(f)
  def wrapper(obj, *args, **kwargs):
    inputs_repr = _get_inputs_repr(args, kwargs)
    object_id = getattr(obj, '_nnx_tabulate_id')
    node_info = node_stats[object_id]
    path = node_info.path
    if method_name != '__call__':
      path = (*path, method_name)
    identifier = (inputs_repr, object_id)
    counter_val = next(counter)
    graphdef, state = nnx.split(((obj, *args), kwargs))
    if compute_flops:
      lowered = jit_f.lower(graphdef, state)
      flops = _get_flops(lowered)
      outputs = lowered.out_info
    else:
      flops = None
      outputs = jit_f(graphdef, state)
    if identifier not in seen:
      seen.add(identifier)
      output_repr = jax.tree.map(_to_dummy_array, outputs)
      vjp_flops = _get_flops(jax.jit(do_vjp).lower(
        obj, *args, **kwargs)) if compute_vjp_flops else None
      tracer_args.append(
        CallInfo(counter_val, object_id, type(obj), path, inputs_repr,
          output_repr, flops, vjp_flops))
    return jit_f(graphdef, state)
  return wrapper

