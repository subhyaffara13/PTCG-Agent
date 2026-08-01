
def register_force_test(
    op: OpType, func_impl: Callable[..., Any] | None = None
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[..., Any]:
    """Will attempt to test these ops even if they err on "normal" inputs"""
    FORCE_TEST_LIST.append(op)
    return register_complex(op, func_impl)

