
def _ragged_dot_general_gpu_lowering(ctx, *args, **kwargs):
  if config.jax_ragged_dot_use_gpu_pallas_triton_lowering.value:
    from jax._src.lax.pallas_lowerings.gpu import ragged_dot

    if ragged_dot._backend_supports_triton(ctx):
      return mlir.lower_fun(ragged_dot._pallas_ragged_dot_general_impl,
                            multiple_results=False)(ctx, *args, **kwargs)
  # fall back to the default gpu lowering
  return _ragged_dot_general_lower(ctx, *args, **kwargs, platform='gpu')

