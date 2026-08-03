from typing import Callable

def register_fast_op_impl(
    func: OpOverload,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    def impl_decorator(op_impl: Callable[_P, _R]) -> Callable[_P, _R]:
        FAST_OP_IMPLEMENTATIONS[func] = op_impl
        return op_impl

    return impl_decorator

