
def assert_no_errors(fn: FuncIR) -> None:
    assert not check_func_ir(fn)

