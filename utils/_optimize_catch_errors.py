
def _optimize_catch_errors(
    compile_fn: convert_frame.ConvertFrameProtocol,
    hooks: Hooks,
    backend_ctx_ctor: Callable[
        [], contextlib.AbstractContextManager[Any]
    ] = null_context,
    fullgraph: bool = False,
    error_on_graph_break: bool | None = None,
    export: bool = False,
    dynamic: bool | None = None,
    compiler_config: Any | None = None,
    rebuild_ctx: Callable[[], OptimizeContext | _NullDecorator] | None = None,
    package: CompilePackage | None = None,
) -> OptimizeContext:
    return OptimizeContext(
        convert_frame.catch_errors_wrapper(compile_fn, hooks),
        backend_ctx_ctor=backend_ctx_ctor,
        first_ctx=True,
        fullgraph=fullgraph,
        error_on_graph_break=error_on_graph_break,
        export=export,
        dynamic=dynamic,
        compiler_config=compiler_config,
        rebuild_ctx=rebuild_ctx,
        package=package,
        hooks=hooks,
    )

