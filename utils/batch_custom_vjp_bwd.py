from typing import Callable

def batch_custom_vjp_bwd(bwd: lu.WrappedFun, tag: core.TraceTag,
                         axis_data: AxisData,
                         in_dims: Callable[[], Sequence[int | None]],
                         out_dim_dests: Sequence[int | None]) -> lu.WrappedFun:
  def new_bwd(*args):
    in_dims_ = in_dims() if callable(in_dims) else in_dims
    args = [SymbolicZero(core.mapped_aval(axis_data.size, dim, x.aval))
            if type(x) is SymbolicZero else x
            for x, dim in zip(args, in_dims_)]
    in_dims_ = [None if type(x) is SymbolicZero else d
                for x, d in zip(args, in_dims_)]
    bwd_, out_dims_thunk = batch_subtrace(bwd, tag, axis_data, in_dims_)
    bwd_ = _match_axes_and_sum(bwd_, axis_data, out_dims_thunk, out_dim_dests)
    return bwd_.call_wrapped(*args)
  return lu.wrap_init(new_bwd, debug_info=bwd.debug_info)

