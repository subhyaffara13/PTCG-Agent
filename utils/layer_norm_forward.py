import functools

def layer_norm_forward(
    x, weight, bias,
    num_warps: int | None = None,
    num_stages: int | None = 3,
    eps: float = 1e-5,
    backward_pass_impl: str = 'triton',
    interpret: bool = False):
  del num_stages
  del backward_pass_impl
  n = x.shape[-1]
  # Triton heuristics
  # Less than 64KB per feature: enqueue fused kernel
  max_fused_size = 65536 // x.dtype.itemsize
  block_size = min(max_fused_size, pl.next_power_of_2(n))
  block_size = min(max(block_size, 128), 4096)
  num_warps = min(max(block_size // 256, 1), 8)

  kernel = functools.partial(layer_norm_forward_kernel, eps=eps,
                             block_size=block_size)
  out_shape = [
          jax.ShapeDtypeStruct(shape=(n,), dtype=x.dtype),
          jax.ShapeDtypeStruct(shape=(), dtype=x.dtype),
          jax.ShapeDtypeStruct(shape=(), dtype=x.dtype)
  ]
  method = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(num_warps=num_warps),
      grid=(),
      out_shape=out_shape,
      debug=False,
      interpret=interpret,
      name="ln_forward",
  )

  method = jax.vmap(jax.vmap(method, in_axes=(0, None, None)), in_axes=(0, None, None))
  out, mean, rstd = method(x, weight, bias)
  return out, (x, weight, bias, mean, rstd)

