from typing import Any, Callable

def _remat_opt_vmap(
    axis_data, args, in_dims,
    *,
    num_consts: int,
    num_res: int,
    fwd_jaxpr: core.ClosedJaxpr,
    fun_jaxpr_thunk: Callable[[], tuple[core.Jaxpr, Sequence[Any]]],
):
  args = [batching.moveaxis(x, d, 0) if d is not None and d != 0
          else x for x, d in zip(args, in_dims)]
  in_batched = [d is not None for d in in_dims]
  batched_fwd_jaxpr, out_batched = batching.batch_jaxpr(
      fwd_jaxpr, axis_data, in_batched, False)
  extra_consts = batched_fwd_jaxpr.consts
  batched_fwd_jaxpr = pe.close_jaxpr(
      pe.convert_constvars_jaxpr(batched_fwd_jaxpr.jaxpr))
  out_dims = [0 if b else None for b in out_batched]

  _, prim_batched = split_list(in_batched, [num_consts])

  @pe._memoize
  def batched_fun_jaxpr_thunk():
    fun_jaxpr = core.ClosedJaxpr(*fun_jaxpr_thunk())
    batched_fun_jaxpr, out_batched = batching.batch_jaxpr(
        fun_jaxpr, axis_data, prim_batched, False)
    return batched_fun_jaxpr.jaxpr, batched_fun_jaxpr.consts

  batched_outs = remat_opt_p.bind(*extra_consts, *args,
                                  num_consts=num_consts + len(extra_consts),
                                  num_res=num_res,
                                  fwd_jaxpr=batched_fwd_jaxpr,
                                  fun_jaxpr_thunk=batched_fun_jaxpr_thunk)

  return batched_outs, out_dims

