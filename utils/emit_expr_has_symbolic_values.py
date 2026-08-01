
def emit_expr_has_symbolic_values(expr: str, type: CType) -> str:
    if type == BaseCType(SymIntT):
        return f"{expr}.is_symbolic()"

    if isinstance(type, OptionalCType):
        innerexpr = f"(*{expr})"
        return f"{expr}.has_value() ? {emit_expr_has_symbolic_values(innerexpr, type.elem)} : false"

    if type == BaseCType(optionalSymIntArrayRefT):
        return emit_expr_has_symbolic_values(
            expr, OptionalCType(BaseCType(symIntArrayRefT))
        )

    if type in (BaseCType(symIntArrayRefT), VectorCType(BaseCType(SymIntT))):
        argname = "arg"
        lambda_check = emit_expr_has_symbolic_values(argname, BaseCType(SymIntT))
        return (
            "std::any_of("
            f"{expr}.begin(), {expr}.end(), "
            f"[=](auto& {argname}) {{ return {lambda_check}; }})"
        )

    raise ValueError(
        "unsupported type for has_symbolic_values check. "
        "It should be a SymInt or a collection of those. "
        f"Got: {type.cpp_type()}"
    )

