
def _get_jax_and_to_jax():
    global _JAX
    if _JAX is None:
        import jax  # type: ignore

        @to_backend_cache_wrap
        @jax.jit
        def to_jax(x):
            return x

        _JAX = jax, to_jax

    return _JAX

