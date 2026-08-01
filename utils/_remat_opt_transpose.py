
def _remat_opt_transpose(
    cts, *args,
    num_consts: int,
    num_res: int,
    fwd_jaxpr: core.ClosedJaxpr,
    fun_jaxpr_thunk: Callable[[], tuple[core.Jaxpr, Sequence[Any]]],
):
  # TODO(dfm): It shouldn't be too hard to implement this as needed in the
  # future.
  raise NotImplementedError(
      "remat optimization for custom_vjp does not support higher-order AD")

