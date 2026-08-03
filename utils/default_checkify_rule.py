from typing import Any

def default_checkify_rule(primitive: core.Primitive, error: Error,
                          enabled_errors, *invals: core.Value,
                          **params: Any) -> tuple[Error, Sequence[core.Value]]:
  """Default rule for primitives in `checkify` interpreter."""
  if 'call_jaxpr' not in params:
    # Default non-HOP case: just call primitive and don't update error.
    return error, primitive.bind(*invals, **params)

  # Code below handles call- and map-primitives, by recursively calling
  # checkify_jaxpr.
  err_vals, err_tree = jtu.tree_flatten(error)
  num_error_vals = len(err_vals)
  if 'donated_invars' in params:
    params = dict(params, donated_invars=(*[False]*num_error_vals,
                                          *params['donated_invars']))

  # call_jaxpr handling
  call_jaxpr = params.pop('call_jaxpr')
  if isinstance(call_jaxpr, core.ClosedJaxpr):  # handle closed_call_p
    jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  else:
    jaxpr, consts = call_jaxpr, ()
  consts_ = tuple(HashableWrapper(c) for c in consts)
  partial_checkify = lu.hashable_partial(
      lu.wrap_init(checkify_jaxpr_flat_hashable, debug_info=jaxpr.debug_info),
      jaxpr, consts_, enabled_errors, err_tree)
  partial_checkify, metadata = _flatten_and_get_error_metadata_thunk(
      partial_checkify)

  all_vals = primitive.bind(*err_vals, *invals, subfuns=(partial_checkify,),
                            **params)

  out_tree, _ = metadata()
  error, out_vals = tree_unflatten(out_tree, all_vals)
  return error, out_vals

