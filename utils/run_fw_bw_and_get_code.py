
def run_fw_bw_and_get_code(fn: Callable[..., Any]) -> tuple[Any, list[str]]:
    def run_with_backward() -> Any:
        result = fn()
        result.sum().backward()
        return result

    return run_and_get_code(run_with_backward)

