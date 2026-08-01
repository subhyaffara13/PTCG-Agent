
def build_error(msg: str) -> NoReturn:
    raise CompileError([f"mypy: error: {msg}"])

