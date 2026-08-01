
def layer_norm_backward(
    num_warps: int | None,
    num_stages: int | None,
    eps: float,
    backward_pass_impl: str,
    interpret: bool,
    res, do):
  del num_stages
  x, weight, bias, mean, rstd = res
  if backward_pass_impl == 'xla':
    return jax.vjp(layer_norm_reference, x, weight, bias)[1](do)

  *shape_prefix, n = x.shape
  reshaped_x = x.reshape((-1, n))
  reshaped_mean = mean.reshape((-1,))
  reshaped_rstd = rstd.reshape((-1,))
  reshaped_do = do.reshape((-1, n))
  # Triton heuristics
  # Less than 64KB per feature: enqueue fused kernel
  max_fused_size = 65536 // x.dtype.itemsize
  block_size = min(max_fused_size, pl.next_power_of_2(n))
  block_size = min(max(block_size, 128), 4096)
  num_warps = min(max(block_size // 256, 1), 8)

  # layer_norm_backward_kernel_dx parallel over batch dims
  kernel = functools.partial(layer_norm_backward_kernel_dx, eps=eps,
                             block_size=block_size)
  out_shape_dx = jax.ShapeDtypeStruct(shape=(n,), dtype=x.dtype)
  method = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(num_warps=num_warps),
      grid=(),
      out_shape=out_shape_dx,
      debug=False,
      interpret=interpret,
      name="ln_backward_dx",
  )

  method = jax.vmap(method, in_axes=(0, None, None, 0, 0, 0))
  dx = method(reshaped_x, weight, bias, reshaped_do, reshaped_mean, reshaped_rstd)
  dx = dx.reshape((*shape_prefix, n))

  # layer_norm_backward_kernel_dw_db reduce over batch dims
  # Triton heuristics
  if n > 10240:
    block_n = 128
    block_m = 32
    num_warps = 4
  else:
    # maximize occupancy for small N
    block_n = 16
    block_m = 16
    num_warps = 8
  kernel = functools.partial(layer_norm_backward_kernel_dw_db, eps=eps,
                             block_m=block_m, block_n=block_n)
  out_shape_dwbias = [
          jax.ShapeDtypeStruct(shape=weight.shape, dtype=weight.dtype),
          jax.ShapeDtypeStruct(shape=bias.shape, dtype=bias.dtype)
  ]
  grid_ = (pl.cdiv(reshaped_x.shape[1], block_n),)
  method = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(num_warps=num_warps),
      grid=grid_,
      out_shape=out_shape_dwbias,
      debug=False,
      interpret=interpret,
      name="ln_backward_dw_db",
  )
  dw, dbias = method(reshaped_x, weight, bias, reshaped_do, reshaped_mean, reshaped_rstd)
  return dx, dw, dbias

