from typing import Any

def dynamo_timed_cudagraph(
    name: str,
    compile_id: CompileId | None,
    mode: CompilationMode | None,
) -> Generator[Any, None, None]:
    """
    Makes usages of dynamo_timed in this file less verbose. NOTE: This CM sums
    all durations into a single column in the dynamo_compile table. Use only if
    you consider the timed region to be part of the runtime overhead associated
    with the compiler.
    """
    with dynamo_timed(
        name,
        log_pt2_compile_event=True,
        compile_id=compile_id,
        is_backward=mode == CompilationMode.BACKWARD,
        dynamo_compile_column_us="runtime_cudagraphify_time_us",
    ):
        yield

