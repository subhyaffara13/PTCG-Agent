
def catch_errors_wrapper(
    callback: ConvertFrameProtocol, hooks: Hooks
) -> CatchErrorsWrapper:
    return CatchErrorsWrapper(callback, hooks)

