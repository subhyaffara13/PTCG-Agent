
def _remat_opt_impl(
    *args,
    num_consts: int,
    num_res: int,
    fwd_jaxpr: core.ClosedJaxpr,
    fun_jaxpr_thunk: Callable[[], tuple[core.Jaxpr, Sequence[Any]]],
):
  del num_consts, num_res, fun_jaxpr_thunk  # unused
  return core.jaxpr_as_fun(fwd_jaxpr)(*args)

