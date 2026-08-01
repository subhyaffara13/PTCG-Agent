
def io_callback_batching_rule(
    args, dims, callback, result_avals, sharding, ordered
):
  from jax._src.lax.control_flow.loops import map as lax_map  # pyrefly: ignore[missing-import]
  if ordered:
    raise ValueError("Cannot `vmap` ordered IO callback.")
  is_batched = [d is not None for d in dims]
  new_args = [arg if dim is None else
              batching.moveaxis(arg, dim, 0) for arg, dim in zip(args, dims)]
  unbatched_args, batched_args = util.partition_list(is_batched, new_args)
  def _batch_fun(batched_args):
    merged = util.merge_lists(is_batched, unbatched_args, batched_args)
    return io_callback_p.bind(*merged, callback=callback, sharding=sharding,
                              result_avals=result_avals, ordered=False)
  out_vals = lax_map(_batch_fun, batched_args)
  return out_vals, (0,) * len(out_vals)

