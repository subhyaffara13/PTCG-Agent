
def custom_remat(f, f1, f2, fbwd, *, static_argnums=(), static_argnames=()):
  helper = custom_derivatives.custom_vjp(lambda _, *args: f(*args))
  helper.defvjp(f2, fbwd)
  def call(*args, **kwargs):
    args_ft = FlatTree.flatten_static_argnums_argnames(
        args, kwargs, static_argnums, static_argnames)
    avals_ft = args_ft.map(typeof)
    dbg = api_util.debug_info(
        'custom_remat', f, args, kwargs, static_argnums=static_argnums,
        static_argnames=static_argnames)
    jaxpr_, out_avals_ft = pe.trace_to_jaxpr(f, avals_ft, dbg)
    jaxpr, consts = pe.separate_consts(jaxpr_)
    out_flat = CustomRemat(jaxpr, f1, helper, args_ft.tree, out_avals_ft.tree)(*consts, *args_ft)
    return out_avals_ft.update(out_flat).unflatten()
  return call

