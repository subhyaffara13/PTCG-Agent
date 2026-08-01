
def register_simple(
    op: OpType,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[..., Any]:
    """Register an op which can be applied independently to the real and complex parts to get the result."""

    def impl(
        self: ComplexTensor, *args: Any, dtype: torch.dtype | None = None, **kwargs: Any
    ) -> ComplexTensor:
        x, y = split_complex_tensor(self)
        if dtype is not None and dtype not in COMPLEX_TO_REAL:
            raise RuntimeError(
                "Non-complex `dtype` specified, please write custom impl."
            )

        if dtype in COMPLEX_TO_REAL:
            if dtype is None:
                raise AssertionError("dtype must not be None when in COMPLEX_TO_REAL")
            kwargs["dtype"] = COMPLEX_TO_REAL[dtype]

        u = op(x, *args, **kwargs)
        v = op(y, *args, **kwargs)

        u_flat, u_spec = tree_flatten(u)
        v_flat, v_spec = tree_flatten(v)
        if u_spec != v_spec:
            raise AssertionError(f"Tree specs must match: {u_spec} != {v_spec}")
        out_flat = [
            ComplexTensor(ui, vi) for ui, vi in zip(u_flat, v_flat, strict=False)
        ]
        return tree_unflatten(out_flat, u_spec)

    func_name = _get_func_name(op)
    impl.__name__ = func_name
    impl.__qualname__ = func_name

    return register_complex(op, impl)

