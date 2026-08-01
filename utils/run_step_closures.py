
def run_step_closures():
    devctx = get_device_context()
    async_step_closures = getattr(devctx, "async_step_closures", None)
    if async_step_closures is not None:
        devctx.async_step_closures = []  # type: ignore[attr-defined]
        async_closure_handler = getattr(devctx, "async_closure_handler", None)
        if async_closure_handler is None:
            async_closure_handler = AsyncClosureHandler()
            devctx.async_closure_handler = async_closure_handler  # type: ignore[attr-defined]
        async_closure_handler(async_step_closures)

    step_closures = getattr(devctx, "step_closures", None)
    if step_closures is not None:
        devctx.step_closures = []  # type: ignore[attr-defined]
        closure_handler = getattr(devctx, "closure_handler", None)
        if closure_handler is None:
            closure_handler = ClosureHandler()
            devctx.closure_handler = closure_handler  # type: ignore[attr-defined]
        closure_handler(step_closures)
    return devctx

