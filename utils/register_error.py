from typing import Any, Callable

def register_error(
    op: OpType, exc_type: type[Exception] = NotImplementedError
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[..., Any]:
    msg = f"`aten.{_get_op_name(op)}` not implemented for `{ComplexTensor.__name__}`."

    def ordered_impl(*args: Any, **kwargs: Any) -> Never:
        raise exc_type(msg)

    func_name = _get_func_name(op)
    ordered_impl.__name__ = func_name
    ordered_impl.__qualname__ = func_name

    return register_force_test(op, ordered_impl)

