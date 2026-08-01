
def assert_has_error(fn: FuncIR, error: FnError) -> None:
    errors = check_func_ir(fn)
    assert errors == [error]

