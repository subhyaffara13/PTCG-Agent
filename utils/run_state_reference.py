from typing import Callable

def run_state_reference(f: Callable[..., None]):
  def wrapped(args):
    dbg = api_util.debug_info("run_state", f, (args,), {})
    flat_args, in_tree = tree_util.tree_flatten(args)
    ref_avals, ref_args = unzip2(map(get_ref_aval_from_value, flat_args))
    jaxpr_, consts, _ = initial_style_jaxpr(f, in_tree, ref_avals, dbg)
    jaxpr = hoist_consts_to_refs(jaxpr_)
    discharged_closed_jaxpr = discharge_state(core.ClosedJaxpr(jaxpr, ()))
    discharged_jaxpr, discharged_consts = discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts

    # Initialize any uninitialized values here in ref_args in the reference.
    ref_args = [
        _default_initialization(aval) if r is uninitialized else r
        for r, aval in zip(ref_args, ref_avals)
    ]

    out_const_flat = core.eval_jaxpr(discharged_jaxpr, discharged_consts,
                                     *consts, *ref_args)
    _, out_flat = split_list(out_const_flat, [len(consts)])
    return in_tree.unflatten(out_flat)
  return wrapped

