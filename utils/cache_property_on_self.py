
def cache_property_on_self(
    fn: Callable[Concatenate[Any, P], RV],
) -> CachedMethod[P, RV]:
    """
    Variant of cache_on_self for properties. The only difference is the type signature.
    """

    return cache_on_self(fn)

