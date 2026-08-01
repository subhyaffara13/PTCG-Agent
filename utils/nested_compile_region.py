
def nested_compile_region(
    fn=None,
    *,
    options: NestedCompileRegionOptions | None = None,
    max_reuse_entries: int = 8,
    reuse_hash_fn=None,
):
    """
    Tells **``torch.compile``** that the marked set of operations forms a nested
    compile region (which is often repeated in the full model) whose code can be
    compiled once and safely reused.  ``nested_compile_region`` can also be used
    as a decorator.

    During **``torch.compile``** tracing, the compiler applies *hierarchical
    compilation* with ``nested_compile_region``: it emits optimized code for the
    marked region the first time it is encountered and re-emits (or "stamps
    out") the previously compiled code on every subsequent invocation.  This can
    substantially reduce overall compile time for deeply-stacked,
    structurally-identical components such as the transformer layers of a
    large-language-model (LLM).

    Outside a ``torch.compile`` context—i.e., in standard eager execution—the
    call is a no-op, so existing workflows remain unaffected.

    Note that ``nested_compile_region`` **does not** promise that a region will
    be compiled exactly once.  If the compiler detects that new input conditions
    (shape, dtype, device, stride, globals etc.) make the cached version invalid
    to reuse, it will transparently re-compile the region.  Using it is
    therefore *safe*: correctness is always preserved, and you pay the extra
    compilation cost only when required.

    Args:
        fn: The function to wrap
        options: Optional backend to use for compiling the subgraph.
            Warning: this is an experimental feature under development and
            not ready for use yet.
        max_reuse_entries: Maximum number of reuse cache entries per function
            before raising an error. If this limit is hit, guards keep failing
            across invocations and hierarchical compilation is not effective.
        reuse_hash_fn: Optional callable that takes the same ``*args, **kwargs``
            as the wrapped function and returns an integer hash key. When
            provided, Dynamo traces this function to obtain a constant integer
            and uses it as the cache key for subgraph reuse, bypassing the
            automatic fingerprint/guard machinery. Two calls that produce the
            same hash key reuse the same cached subgraph. The hash function
            must be fully traceable (no graph breaks) and must return a
            constant integer.
    """

    if options is not None:
        from torch._dynamo import config as dynamo_config

        if not dynamo_config.enable_invoke_subgraph_regional_compile:
            raise RuntimeError(
                "nested_compile_region config is an experimental feature for testing only."
            )

    from torch._higher_order_ops.invoke_subgraph import (
        mark_compile_region as _mark_compile_region,
    )

    return _mark_compile_region(
        fn,
        options=options,
        max_reuse_entries=max_reuse_entries,
        reuse_hash_fn=reuse_hash_fn,
    )

