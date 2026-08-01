
def maybe_replace_cumulative_out_dtype_exprs(
    f: NativeFunction,
    functional_sig: DispatcherSignature,
    functional_exprs: list[str],
) -> list[str]:
    if (
        f.func.kind() != SchemaKind.out
        or f.func.name not in CUMULATIVE_OUT_OPS_PRESERVING_OUT_DTYPE
    ):
        return functional_exprs

    if len(f.func.arguments.out) != 1:
        raise AssertionError(
            f"Expected a single out argument for cumulative out op: {f.func.name}"
        )

    dtype_arg_idx = next(
        (i for i, arg in enumerate(functional_sig.arguments()) if arg.name == "dtype"),
        None,
    )
    if dtype_arg_idx is None:
        raise AssertionError(
            f"Expected dtype argument for cumulative out op: {f.func.name}"
        )

    adjusted_exprs = functional_exprs.copy()
    dtype_expr = adjusted_exprs[dtype_arg_idx]
    adjusted_exprs[dtype_arg_idx] = (
        f"{dtype_expr}.has_value() ? {dtype_expr} : "
        f"std::optional<at::ScalarType>({f.func.arguments.out[0].name}_.scalar_type())"
    )
    return adjusted_exprs

