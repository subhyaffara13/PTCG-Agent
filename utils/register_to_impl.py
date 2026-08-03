from typing import Any, Callable

def register_to_impl(op: OpType) -> Callable[..., Any]:
    """Register an op similar to `aten.to`, but may have different signatures."""

    def impl(
        self: ComplexTensor, *args: Any, **kwargs: Any
    ) -> torch.Tensor | ComplexTensor:
        x, y = split_complex_tensor(self)
        try:
            args = tuple(_dt_to_real(a) for a in args)
            kwargs = {k: _dt_to_real(v) for k, v in kwargs.items()}
        except KeyError:
            return op(x, *args, **kwargs)

        return ComplexTensor(op(x, *args, **kwargs), op(y, *args, **kwargs))

    func_name = _get_func_name(op)
    impl.__name__ = func_name
    impl.__qualname__ = func_name

    return register_complex(op, impl)

