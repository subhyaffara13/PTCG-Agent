
def get_structured_logging_overhead() -> float | None:
    key = None
    if (trace_id := torch._guards.CompileContext.current_trace_id()) is not None:
        frame_id = trace_id.compile_id.frame_id
        frame_compile_id = trace_id.compile_id.frame_compile_id
        key = f"{frame_id}_{frame_compile_id}"
    if key is not None:
        return structured_logging_overhead.get(key)
    else:
        return None

