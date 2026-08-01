
def assert_func_ir_valid(fn: FuncIR) -> None:
    errors = check_func_ir(fn)
    if errors:
        raise IrCheckException(
            "Internal error: Generated invalid IR: \n"
            + "\n".join(format_func(fn, [(e.source, e.desc) for e in errors]))
        )

