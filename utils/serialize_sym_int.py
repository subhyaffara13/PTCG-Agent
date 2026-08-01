
def serialize_sym_int(s: int | torch.SymInt) -> SymInt:
    if isinstance(s, (torch.SymInt, sympy.Symbol, int)):
        if symbolic_shapes.is_concrete_int(s):
            return SymInt.create(as_int=int(s))
        else:
            if not isinstance(s, (torch.SymInt, sympy.Symbol)):
                raise AssertionError(
                    f"expected SymInt or Symbol, got {type(s).__name__}"
                )
            if s.node.hint is None:
                return SymInt.create(as_expr=SymExpr(_print_sympy(s)))
            else:
                return SymInt.create(
                    as_expr=SymExpr(
                        _print_sympy(s),
                        hint=SymExprHint.create(as_int=s.node.hint),
                    )
                )
    else:
        raise SerializeError(
            f"SymInt should be either symbol or int, got `{s}` of type `{type(s)}`"
        )

