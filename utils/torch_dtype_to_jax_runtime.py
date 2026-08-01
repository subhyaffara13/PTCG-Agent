
def torch_dtype_to_jax_runtime(dtype: torch.dtype) -> Any:
    """
    Map PyTorch dtype to actual JAX dtype object at runtime.

    This helper is used in generated Pallas kernels at runtime to convert
    PyTorch dtypes to JAX dtype objects (not string representations).

    Args:
        dtype: PyTorch dtype to convert

    Returns:
        JAX dtype object (e.g., jnp.float32 object itself)
    """
    import jax.numpy as jnp  # pyrefly: ignore [import-error, missing-import]

    dtype_map = {
        torch.float32: jnp.float32,
        torch.float64: jnp.float64,
        torch.float16: jnp.float16,
        torch.bfloat16: jnp.bfloat16,
        torch.int32: jnp.int32,
        torch.int64: jnp.int64,
        torch.int16: jnp.int16,
        torch.int8: jnp.int8,
        torch.uint8: jnp.uint8,
        torch.bool: jnp.bool_,
        torch.complex64: jnp.complex64,
        torch.complex128: jnp.complex128,
    }
    if dtype not in dtype_map:
        raise ValueError(f"Unsupported dtype for JAX conversion: {dtype}")
    return dtype_map[dtype]

