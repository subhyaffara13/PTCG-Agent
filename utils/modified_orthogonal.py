
def modified_orthogonal(key: Array, shape: Shape, dtype: Dtype = jnp.float32) -> Array:
    """Modified orthogonal initializer for compatibility with half precision."""
    initializer = initializers.orthogonal()
    return initializer(key, shape).astype(dtype)

