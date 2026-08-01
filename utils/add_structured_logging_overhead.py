
def add_structured_logging_overhead(time_spent: float) -> None:
    global structured_logging_overhead
    key = None
    if (trace_id := torch._guards.CompileContext.current_trace_id()) is not None:
        frame_id = trace_id.compile_id.frame_id
        frame_compile_id = trace_id.compile_id.frame_compile_id
        # Why not trace_id.attempt, like structured logging?
        # We aggregate across all attempts because
        # a compilation metric is logged per successful attempt
        key = f"{frame_id}_{frame_compile_id}"
    # TODO: deal with structured logging that occurs outside of specific compile ids
    # It's hard to figure out where we would log that if we want it in compilation metrics
    # itself.
    if key is not None:
        key = str(key)
        structured_logging_overhead[key] += time_spent

