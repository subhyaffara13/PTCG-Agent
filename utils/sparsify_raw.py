from typing import Any

def sparsify_raw(f):

  def wrapped(
      spenv: SparsifyEnv, *spvalues: SparsifyValue, **params: Any
  ) -> tuple[Sequence[SparsifyValue], pytree.PyTreeDef]:
    spvalues_flat, in_tree = tree_flatten(spvalues, is_leaf=_is_spvalue)
    in_avals_flat = spvalues_to_avals(spenv, spvalues_flat)
    wrapped_fun, out_tree = flatten_fun_nokwargs(
        lu.wrap_init(
            f, params,
            debug_info=api_util.debug_info("sparsify", f,
                                           in_tree.unflatten([True] * len(in_avals_flat)),
                                           {})),
        in_tree)
    jaxpr, out_avals_flat, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, in_avals_flat)
    result = eval_sparse(jaxpr, consts, spvalues_flat, spenv)
    if len(out_avals_flat) != len(result):
      raise Exception("Internal: eval_sparse does not return expected number of arguments. "
                      "Got {result} for avals {out_avals_flat}")
    return result, out_tree()

  return wrapped

