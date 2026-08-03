from typing import Callable

def register_op_impl(
    run_impl_check: Callable[[OpOverload], bool]
    | OpOverload
    | list[OpOverload]
    | tuple[OpOverload, ...],
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    def impl_decorator(op_impl: Callable[_P, _R]) -> Callable[_P, _R]:
        if isinstance(run_impl_check, OpOverload):
            if run_impl_check in op_implementations_dict:
                raise AssertionError(f"duplicate registration: {run_impl_check}")
            op_implementations_dict[run_impl_check] = op_impl
        elif isinstance(run_impl_check, (list, tuple)):
            for op in run_impl_check:
                register_op_impl(op)(op_impl)
        else:
            if not callable(run_impl_check):
                raise AssertionError(
                    f"run_impl_check must be callable, got {type(run_impl_check)}"
                )
            op_implementations_checks.append((run_impl_check, op_impl))

        return op_impl

    return impl_decorator

