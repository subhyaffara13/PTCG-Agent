
def _patch_einops_symint_compat(einops_mod: Any) -> None:
    """Backport the SymInt lru_cache fix from einops 0.7.0 into einops <= 0.6.1."""
    for name in ("_reconstruct_from_shape", "_prepare_transformation_recipe"):
        cached = getattr(einops_mod, name)
        uncached = cached.__wrapped__

        def make_wrapper(cached_fn: Any, uncached_fn: Any) -> Any:
            @functools.wraps(cached_fn)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return cached_fn(*args, **kwargs)
                except TypeError:
                    return uncached_fn(*args, **kwargs)

            return wrapper

        setattr(einops_mod, name, make_wrapper(cached, uncached))

