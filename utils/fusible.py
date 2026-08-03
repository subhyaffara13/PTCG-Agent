from typing import Any

def fusible(f=None, *, output_fusion_prefix: Any = True):
  def decorator(f):
    def wrapper(*args):
      def wrapped(*args):
        in_fusions = tree_util.tree_map(_make_trivial_fusion, args)
        output_fusions = tree_util.tree_unflatten(
            tree_util.tree_structure(output_fusion_prefix),
            [None] * len(tree_util.tree_leaves(output_fusion_prefix)),
        )
        return f(*in_fusions, output_fusions)

      flat_args, in_tree = tree_util.tree_flatten(args)
      debug_info = api_util.debug_info('fusible', wrapped, args, {})
      flat_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
          lu.wrap_init(wrapped, debug_info=debug_info), in_tree
      )
      flat_avals = [jax_core.typeof(x) for x in flat_args]
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, flat_avals)
      out_tree = out_tree_thunk()
      out = fusible_p.bind(
          *consts,
          *flat_args,
          jaxpr=jaxpr,
          num_consts=len(consts),
          in_tree=in_tree,
          out_tree=out_tree,
          func=f,
          output_fusion_prefix=output_fusion_prefix,
      )
      return tree_util.tree_unflatten(out_tree, out)

    return wrapper

  if f is not None:
    return decorator(f)
  return decorator

