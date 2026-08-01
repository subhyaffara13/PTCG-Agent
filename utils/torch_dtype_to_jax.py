
def torch_dtype_to_jax(dtype: torch.dtype) -> str:
    """
    Map PyTorch dtype to JAX dtype expression string.

    This helper is used at compile time in codegen to generate
    JAX dtype expressions for Pallas kernels.

    Args:
        dtype: PyTorch dtype to convert

    Returns:
        JAX dtype expression as string (e.g., "jnp.float32")
    """
    jax_dtype = torch_dtype_to_jax_runtime(dtype)
    dtype_name = jax_dtype.__name__
    if dtype_name == "bool":
        dtype_name = "bool_"
    return f"jnp.{dtype_name}"

