import functools

def rms_norm(
    input: Tensor,
    normalized_shape: list[int],
    weight: Tensor | None = None,
    eps: float | None = None,
) -> Tensor:
    r"""Apply Root Mean Square Layer Normalization.

    See :class:`~torch.nn.RMSNorm` for details.
    """
    if has_torch_function_variadic(input, weight):
        return handle_torch_function(
            rms_norm, (input, weight), input, normalized_shape, weight=weight, eps=eps
        )
    return torch.rms_norm(input, normalized_shape, weight, eps)


def rms_norm(
    x, weight, bias,
    num_warps: int | None = None,
    num_stages: int | None = 3,
    eps: float = 1e-5,
    backward_pass_impl: str = 'triton',
    interpret: bool = False):
  n = x.shape[-1]
  # Triton heuristics
  # Less than 64KB per feature: enqueue fused kernel
  max_fused_size = 65536 // x.dtype.itemsize
  block_size = min(max_fused_size, pl.next_power_of_2(n))
  block_size = min(max(block_size, 128), 4096)
  num_warps = min(max(block_size // 256, 1), 8)

  kernel = functools.partial(rms_norm_forward_kernel, eps=eps,
                             block_size=block_size)
  out_shape = jax.ShapeDtypeStruct(shape=(n,), dtype=x.dtype)
  method = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(
          num_warps=num_warps, num_stages=num_stages
      ),
      grid=(),
      out_shape=out_shape,
      debug=False,
      interpret=interpret,
  )
  method = jax.vmap(jax.vmap(method, in_axes=(0, None, None)), in_axes=(0, None, None))
  return method(x, weight, bias)

