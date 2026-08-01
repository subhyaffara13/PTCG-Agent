
def _jax_namespace(api_version: str | None, use_compat: bool | None) -> Namespace:
    if use_compat:
        raise ValueError("JAX does not have an array-api-compat wrapper")
    import jax.numpy as jnp
    if not hasattr(jnp, "__array_namespace_info__"):
        # JAX v0.4.32 and newer implements the array API directly in jax.numpy.
        # For older JAX versions, it is available via jax.experimental.array_api.
        # jnp.Array objects gain the __array_namespace__ method.
        import jax.experimental.array_api  # noqa: F401
    # Test api_version
    return jnp.empty(0).__array_namespace__(api_version=api_version)

