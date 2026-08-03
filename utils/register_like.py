from typing import Any, Callable

def register_like(op: OpType) -> Callable[..., Any]:
    def impl(
        self: ComplexTensor, *args: Any, dtype: torch.dtype | None = None, **kwargs: Any
    ) -> torch.Tensor | ComplexTensor:
        self_re, self_im = split_complex_tensor(self)

        if dtype is not None and dtype not in COMPLEX_TO_REAL:
            return op(self_re, *args, dtype=dtype, **kwargs)

        if dtype is not None:
            kwargs["dtype"] = COMPLEX_TO_REAL[dtype]

        ret_re = op(self_re, *args, **kwargs)
        ret_im = op(self_im, *args, **kwargs)

        return ComplexTensor(ret_re, ret_im)

    func_name = _get_func_name(op)
    impl.__name__ = func_name
    impl.__qualname__ = func_name

    return register_complex(op, impl)

