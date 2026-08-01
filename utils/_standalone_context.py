
def _standalone_context(gm: GraphModule, dynamic_shapes: Any, aot: bool):
    from torch.compiler._cache import CacheArtifactManager

    fake_mode = _resolve_fake_mode(gm, dynamic_shapes)
    tracing_context = torch._guards.TracingContext(fake_mode)
    with (
        torch._guards.tracing(tracing_context),
        CacheArtifactManager.with_fresh_cache(),
        config.patch("triton.autotune_at_compile_time", True),
        torch._functorch.config.patch("bundled_autograd_cache", aot),
    ):
        yield

