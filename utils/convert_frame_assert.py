from typing import Any

def convert_frame_assert(
    compiler_fn: CompilerFn,
    one_graph: bool = True,
    export: bool = False,
    export_constraints: Any | None = None,
    package: CompilePackage | None = None,
    recompile_limit: int | None = None,
) -> ConvertFrameAssert:
    """Fully convert a frame into an FX graph, raising an exception if we fail."""
    return ConvertFrameAssert(
        compiler_fn,
        one_graph,
        export,
        export_constraints,
        package,
        recompile_limit,
    )

