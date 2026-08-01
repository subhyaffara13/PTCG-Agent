
def convert_frame(
    compiler_fn: CompilerFn,
    hooks: Hooks,
    package: CompilePackage | None = None,
    recompile_limit: int | None = None,
) -> ConvertFrame:
    """Try to convert a frame into an FX graph, if error leave frame unmodified"""
    return ConvertFrame(
        compiler_fn, hooks, package=package, recompile_limit=recompile_limit
    )

