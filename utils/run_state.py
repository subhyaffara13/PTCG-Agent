from typing import Callable

def run_state(f: Callable[..., None]) -> Callable[[T], T]:
  def wrapped(args):
    dbg = api_util.debug_info("run_state", f, (args,), {})
    flat_args, in_tree = tree_util.tree_flatten(args)
    ref_avals, ref_args = unzip2(map(get_ref_aval_from_value, flat_args))
    # There may be some uninitialized values here in ref_args.
    jaxpr_, consts, _ = initial_style_jaxpr(f, in_tree, ref_avals, dbg)
    jaxpr = hoist_consts_to_refs(jaxpr_)
    which_linear = (False,) * (len(consts) + len(ref_args))
    refs_is_initialized = tuple(r is not uninitialized for r in ref_args)
    init_args = tuple(r for r in ref_args if r is not uninitialized)
    # Consts are always initialized.
    is_initialized = (True,) * len(consts) + refs_is_initialized
    out_const_flat = run_state_p.bind(*consts, *init_args, jaxpr=jaxpr,
                                      which_linear=which_linear,
                                      is_initialized=is_initialized)
    _, out_flat = split_list(out_const_flat, [len(consts)])
    return in_tree.unflatten(out_flat)
  return wrapped

