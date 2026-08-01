
def guard_error_hook(
    guard_manager: GuardFn,
    code: types.CodeType,
    f_locals: dict[str, object],
    index: int,
    last: bool,
) -> None:
    print(
        f"ERROR RUNNING GUARDS {code.co_name} {code.co_filename}:{code.co_firstlineno}"
    )
    print("lambda " + ", ".join(guard_manager.args) + ":")
    print(" ", " and\n  ".join(guard_manager.code_parts))

    print(guard_manager)

    local_scope = {"L": f_locals, **guard_manager.closure_vars}
    for guard in guard_manager.code_parts:
        try:
            eval(guard, guard_manager.global_scope, local_scope)
        except:  # noqa: B001,E722
            print(f"Malformed guard:\n{guard}")

