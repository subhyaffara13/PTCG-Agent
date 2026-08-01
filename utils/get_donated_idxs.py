
def get_donated_idxs() -> list[int] | None:
    tracing_context = torch._guards.TracingContext.try_get()
    if tracing_context is not None and tracing_context.fw_metadata:
        return tracing_context.fw_metadata.bw_donated_idxs
    return None

