
def wrap_guarded_code(guarded_code: GuardedCode) -> ConvertFrameReturn:
    return ConvertFrameReturn(
        frame_exec_strategy=FrameExecStrategy(FrameAction.DEFAULT, FrameAction.DEFAULT),
        guarded_code=guarded_code,
    )

