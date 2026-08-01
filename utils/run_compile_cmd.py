
def run_compile_cmd(cmd_line: str, cwd: str) -> None:
    with dynamo_timed("compile_file"):
        _run_compile_cmd(cmd_line, cwd)

