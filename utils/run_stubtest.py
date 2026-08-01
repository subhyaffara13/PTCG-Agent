
def run_stubtest(
    stub: str, runtime: str, options: list[str], config_file: str | None = None
) -> str:
    return run_stubtest_with_stderr(stub, runtime, options, config_file)[0]

