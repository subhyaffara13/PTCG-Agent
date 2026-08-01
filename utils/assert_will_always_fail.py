
def assert_will_always_fail(s: AssertStmt, options: Options) -> bool:
    return infer_condition_value(s.expr, options) in (ALWAYS_FALSE, MYPY_FALSE)

