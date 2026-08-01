
def maybe_get_suppress_shape_guards_ctx() -> contextlib.AbstractContextManager[None]:
    # Try to get TracingContext.try_get().fake_mode.shape_env.suppress_guards()
    # If it's not available, return a nullcontext.

    # If we're dealing with cudagraphs, we might not have a tracing_context
    tracing_context = torch._guards.TracingContext.try_get()
    if not tracing_context:
        return contextlib.nullcontext()

    # In standalone inductor compile mode, we might not have a shape_env attached to the fake mode
    if not tracing_context.fake_mode or not tracing_context.fake_mode.shape_env:
        return contextlib.nullcontext()
    shape_env = tracing_context.fake_mode.shape_env
    return shape_env.suppress_guards()

