
def scipy_namespace_for(xp: ModuleType) -> ModuleType | None:
    """Return the `scipy`-like namespace of a non-NumPy backend

    That is, return the namespace corresponding with backend `xp` that contains
    `scipy` sub-namespaces like `linalg` and `special`. If no such namespace
    exists, return ``None``. Useful for dispatching.
    """

    if is_cupy(xp):
        import cupyx  # type: ignore[import-not-found,import-untyped]
        return cupyx.scipy

    if is_jax(xp):
        import jax  # type: ignore[import-not-found]
        return jax.scipy

    if is_torch(xp):
        return xp

    return None

