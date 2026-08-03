from typing import Any, Callable

def register_binary_linear(op: OpType) -> Callable[..., Any]:
    def impl_with_alpha(
        lhs: ComplexTensor,
        rhs: ComplexTensor,
        *args: Any,
        alpha: int | float | complex,
        **kwargs: Any,
    ) -> ComplexTensor:
        return op(lhs, aten.mul(rhs, alpha, *args, **kwargs), *args, **kwargs)

    def impl(
        lhs: ComplexTensor, rhs: ComplexTensor, *args: Any, **kwargs: Any
    ) -> ComplexTensor:
        alpha = kwargs.pop("alpha", None)
        if alpha is not None:
            return impl_with_alpha(lhs, rhs, *args, alpha=alpha, **kwargs)
        a_r, a_i = split_complex_arg(lhs)
        b_r, b_i = split_complex_arg(rhs)
        out_dt, (a_r, a_i, b_r, b_i) = promote_tensors(a_r, a_i, b_r, b_i)
        u = op(a_r, b_r, *args, **kwargs)
        v = op(a_i, b_i, *args, **kwargs)
        return ComplexTensor(u.to(out_dt), v.to(out_dt))

    return register_complex(op, impl)

