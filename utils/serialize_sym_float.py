
def serialize_sym_float(s: float | torch.SymFloat) -> SymFloat:
    if isinstance(s, (torch.SymFloat, sympy.Symbol, float)):
        if symbolic_shapes.is_concrete_float(s):
            return SymFloat.create(as_float=float(s))
        else:
            if not isinstance(s, (torch.SymFloat, sympy.Symbol)):
                raise AssertionError(
                    f"expected SymFloat or Symbol, got {type(s).__name__}"
                )
            if s.node.hint is None:
                return SymFloat.create(as_expr=SymExpr(_print_sympy(s)))
            else:
                return SymFloat.create(
                    as_expr=SymExpr(
                        _print_sympy(s),
                        hint=SymExprHint.create(as_float=s.node.hint),
                    )
                )
    else:
        raise SerializeError(
            f"SymFloat should be either symbol or float, got `{s}` of type `{type(s)}`"
        )

