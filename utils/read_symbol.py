
def read_symbol(data: ReadBuffer, tag: Tag) -> SymbolNode:
    # The branches here are ordered manually by type "popularity".
    if tag == VAR:
        return Var.read(data)
    if tag == FUNC_DEF:
        return FuncDef.read(data)
    if tag == DECORATOR:
        return Decorator.read(data)
    if tag == OVERLOADED_FUNC_DEF:
        return OverloadedFuncDef.read(data)
    if tag == TYPE_VAR_EXPR:
        return TypeVarExpr.read(data)
    if tag == TYPE_ALIAS:
        return TypeAlias.read(data)
    if tag == PARAM_SPEC_EXPR:
        return ParamSpecExpr.read(data)
    if tag == TYPE_VAR_TUPLE_EXPR:
        return TypeVarTupleExpr.read(data)
    assert False, f"Unknown symbol tag {tag}"

