
def _transpose_eval_rule(
    eval_ctx: KernelEvalContext, x, permutation: tuple[int, ...]
):
  block_spec = eval_ctx.out_block_specs[0]
  block_shape = block_spec.block_shape
  block_shape_no_nones = tuple(
      bs
      for bs in block_shape
      if not (bs is None or isinstance(bs, pallas_core.Squeezed))
  )
  block_dims_iter = iter(range(len(block_shape_no_nones)))
  expanded_block_dims = [
      None
      if (bs is None or isinstance(bs, pallas_core.Squeezed))
      else next(block_dims_iter)
      for bs in block_shape
  ]
  assert next(block_dims_iter, None) is None
  permuted_block_dims = [expanded_block_dims[p] for p in permutation]
  new_permutation = [p for p in permuted_block_dims if p is not None]
  return jax.lax.transpose(x, permutation=new_permutation)

