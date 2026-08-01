
def approx_tanh(x: jax.Array) -> jax.Array:
  r"""Elementwise approximate hyperbolic tangent: :math:`\mathrm{tanh}(x)`.

  See
  https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#floating-point-instructions-tanh.
  """
  if x.dtype == jnp.float16:
    asm = "tanh.approx.f16 $0, $1;"
    constraint = "h"
  elif x.dtype == jnp.bfloat16:
    asm = "tanh.approx.bf16 $0, $1;"
    constraint = "h"
  elif x.dtype == jnp.float32:
    asm = "tanh.approx.f32 $0, $1;"
    constraint = "f"
  elif x.dtype == jnp.float64:
    # f64 tanh.approx is only supported on ROCm (uses __ocml_tanh_f64)
    # CUDA does not have a PTX instruction for f64 approximate tanh
    asm = "tanh.approx.f64 $0, $1;"
    constraint = "d"
  else:
    raise TypeError(f"approx_tanh does not accept {x.dtype} arrays")

  [result] = elementwise_inline_asm(
      asm,
      args=[x],
      constraints=f"={constraint},{constraint}",
      pack=1,
      result_shape_dtypes=[jax.ShapeDtypeStruct.like(x)],
  )
  return result

