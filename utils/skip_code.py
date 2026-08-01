
def skip_code(code: types.CodeType) -> None:
    set_code_exec_strategy(
        code, FrameExecStrategy(FrameAction.SKIP, FrameAction.DEFAULT)
    )

