from typing import Callable

def saved_residuals(f: Callable,
                    *args, **kwargs) -> list[tuple[core.AbstractValue, str]]:
  in_leaves, in_tree = tree_flatten((args, kwargs))

  def f_(*args):
    args, kwargs = tree_unflatten(in_tree, args)
    return f(*args, **kwargs)

  debug_info = api_util.debug_info("saved_residuals", f, args, kwargs)
  out = api.make_jaxpr(lambda *args: api.vjp(f_, *args),
                       return_shape=True)(*in_leaves)
  assert isinstance(out, tuple)
  jaxpr_, out_shape_ = out
  jaxpr = jaxpr_.jaxpr
  out_shape = out_shape_[1]
  num_res = tree_structure(out_shape).num_leaves
  jaxpr = jaxpr.replace(
      outvars=jaxpr.outvars[len(jaxpr.outvars) - num_res:],
      debug_info=debug_info._replace(result_paths=None))
  assert len(jaxpr.invars) == len(in_leaves)
  return _saved_residuals(jaxpr, debug_info.arg_names or ("unknown",) * len(jaxpr.invars))

