
def build_guard_function(code_parts: list[str], closure_args: str) -> tuple[str, str]:
    from torch._inductor.utils import IndentedBuffer

    csepass = PyExprCSEPass()
    try:
        csepass.count(code_parts)

        def replace(expr: str) -> tuple[list[str], str]:
            return csepass.replace(expr)

    except RecursionError:
        # If we hit recursion limits during CSE analysis, fall back to a no-op replace function
        # This can happen with extremely complex guard expressions
        def replace(expr: str) -> tuple[list[str], str]:
            return [], expr

    # Generate the inner body of the guard function.
    # i.e. if-chain of the guard expressions.
    guard_body = IndentedBuffer()
    for expr in code_parts:
        preface, expr = replace(expr)
        guard_body.writelines(preface)
        guard_body.writeline(f"if not ({expr}):")
        with guard_body.indent():
            guard_body.writeline("return False")

    # Wrap the inner body into the actual guard function.
    guard = IndentedBuffer()
    guard.writeline("def guard(L):")
    with guard.indent():
        guard.splice(guard_body)
        guard.writeline("return True")

    # Wrap the whole guard function into another function
    # with the closure variables.
    make_guard_fn = IndentedBuffer()
    make_guard_fn.writeline(f"def ___make_guard_fn({closure_args}):")
    with make_guard_fn.indent():
        make_guard_fn.splice(guard)
        make_guard_fn.writeline("return guard")

    return guard_body.getvalue(), make_guard_fn.getvalue()

