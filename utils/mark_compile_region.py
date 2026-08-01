
def mark_compile_region(
    fn=None,
    options: NestedCompileRegionOptions | None = None,
    max_reuse_entries: int = 8,
    reuse_hash_fn=None,
):
    """
    This wrapper instructs torch.compile to compile the wrapped region once and
    reuse the compiled artifact, instead of the usual way of aggressively
    inlining the function.

    Under the hood, it tells TorchDynamo to use InvokeSubgraph HOP for the
    region. For PyTorch eager, this is a no-op.

    Args:
        fn: The function to wrap
        options: Optional config to use for compiling the subgraph.
            Warning: this is an experimental feature under development and
            not ready for use yet.
        max_reuse_entries: Maximum number of reuse cache entries per function
            before raising an error. If this limit is hit, guards keep failing
            across invocations and hierarchical compilation is not effective.
    """

    def wrap(func):
        def inner(*args, **kwargs):
            # Get the innermost function to avoid nested compile regions
            inner_func = func
            while hasattr(inner_func, "__marked_compile_region_fn__"):
                inner_func = inner_func.__marked_compile_region_fn__
            return invoke_subgraph_placeholder(inner_func, *args, **kwargs)

        inner.__marked_compile_region_fn__ = func  # type: ignore[attr-defined]
        func.__marked_compile_region_config__ = options  # type: ignore[attr-defined]
        func.__marked_compile_region_max_reuse_entries__ = max_reuse_entries  # type: ignore[attr-defined]
        func.__marked_compile_region_reuse_hash_fn__ = reuse_hash_fn  # type: ignore[attr-defined]

        return inner

    if fn:
        return wrap(fn)
    else:
        return wrap

