
def infer_scale_swizzle_ir(
    mat: Buffer,
    scale: Buffer,
    transpose: bool = False,
) -> tuple[Any | None, Any | None]:
    """
    Infer the scaling type and swizzle mode for IR nodes (used during graph lowering).

    This is the IR-compatible version of infer_scale_swizzle, using symbolic
    size comparisons via V.graph.sizevars.statically_known_equals.
    """
    from torch._inductor.virtualized import V

    mat_size = mat.get_size()
    scale_size = scale.get_size()

    # Handle transposed matrix
    if transpose:
        mat_size = (mat_size[1], mat_size[0])

    # Compute scale numel symbolically
    scale_numel = functools.reduce(operator.mul, scale_size, 1) if scale_size else 1

    def symbolic_eq(a: Any, b: Any) -> bool:
        """Compare values using symbolic equality when possible."""
        return V.graph.sizevars.statically_known_equals(a, b)

    return _infer_scale_swizzle_impl(
        mat_size=(mat_size[0], mat_size[1]) if len(mat_size) >= 2 else (mat_size[0], 1),
        scale_size=tuple(scale_size),
        scale_numel=scale_numel,
        mat_dtype=mat.dtype,
        scale_dtype=scale.dtype,
        eq_fn=symbolic_eq,
    )

