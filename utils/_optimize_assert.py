from typing import Any, Callable

def _optimize_assert(
    rebuild_ctx: Callable[[], OptimizeContext],
    backend: str | Callable[..., Any] | None,
    *,
    hooks: Hooks = Hooks(None, None, None),
    export: bool = False,
    export_constraints: Any | None = None,
    dynamic: bool | None = None,
    package: CompilePackage | None = None,
    recompile_limit: int | None = None,
) -> OptimizeContext:
    """
    Guarantees single-graph capture.
    The same as `torch._dynamo.optimize(backend)` but ignores
    symbolic_convert.error_on_graph_break setting.

    Used for fullgraph=True and export, since we must always error on graph breaks and ignore
    symbolic_convert.error_on_graph_break. Can also be used for testing.
    """
    backend = get_compiler_fn(backend)

    # Find if backend has any extra context manager
    backend_ctx_ctor = getattr(backend, "backend_ctx_ctor", null_context)

    if config.caching_precompile and package is None:
        # Create an uninitialized package that will be set/filled by
        # _OptimizeContext.__call__
        # We need to instantiate the object here because the same CompilePackage
        # needs to be shared between convert_frame_assert
        # and OptimizeContext.
        from .package import CompilePackage

        package = CompilePackage(fn=None, dynamo=None, ignore_inlined_sources=False)

    return _optimize_catch_errors(
        convert_frame.convert_frame_assert(
            backend,
            export=export,
            export_constraints=export_constraints,
            package=package,
            recompile_limit=recompile_limit,
        ),
        hooks,
        backend_ctx_ctor,
        fullgraph=True,
        export=export,
        dynamic=dynamic,
        rebuild_ctx=rebuild_ctx,
        package=package,
    )

