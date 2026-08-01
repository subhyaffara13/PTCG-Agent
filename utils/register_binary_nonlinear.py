
def register_binary_nonlinear(
    op: OpType,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[..., Any]:
    """Register a "multiplication-style" op, e.g. aten.mul, aten.mm, ..."""

    def impl(
        lhs: ComplexTensor, rhs: ComplexTensor, *args: Any, **kwargs: Any
    ) -> ComplexTensor:
        a_r, a_i = split_complex_arg(lhs)
        b_r, b_i = split_complex_arg(rhs)
        out_dt, (a_r, a_i, b_r, b_i) = promote_tensors(a_r, a_i, b_r, b_i)
        real = op(a_r, b_r, *args, **kwargs) - op(a_i, b_i, *args, **kwargs)
        imag = op(a_r, b_i, *args, **kwargs) + op(a_i, b_r, *args, **kwargs)
        return ComplexTensor(real.to(out_dt), imag.to(out_dt))

    func_name = _get_func_name(op)
    impl.__name__ = func_name
    impl.__qualname__ = func_name

    return register_complex(op, impl)

