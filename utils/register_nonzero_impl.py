from typing import Any, Callable

def register_nonzero_impl(op: OpType) -> Callable[..., Any]:
    def nonzero_impl(
        self: ComplexTensor, other: ComplexTensor, *args: Any, **kwargs: Any
    ) -> torch.Tensor:
        return op(elemwise_nonzero(self), elemwise_nonzero(other), *args, **kwargs)

    func_name = _get_func_name(op)
    nonzero_impl.__name__ = func_name
    nonzero_impl.__qualname__ = func_name

    return register_complex(op, nonzero_impl)

