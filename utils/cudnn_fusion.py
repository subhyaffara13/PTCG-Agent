
def cudnn_fusion(f):
  """Makes a function become a cuDNN kernel. Relies on XLA's handling of
  custom fusions with __cudnn$fusion backend. Currently limited to GEMM
  fusions. For example - batch matmul with mixed types and addition:

  @cudnn_fusion
  def fn(x, y, z):
      return jnp.float32(jax.lax.batch_matmul(jnp.bfloat16(x), y)) + z
  """
  return functools.partial(call_cudnn_fusion, f)

