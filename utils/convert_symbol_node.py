
def convert_symbol_node(self: SymbolNode, cfg: Config) -> Json:
    if isinstance(self, FuncDef):
        return convert_func_def(self)
    elif isinstance(self, OverloadedFuncDef):
        return convert_overloaded_func_def(self)
    elif isinstance(self, Decorator):
        return convert_decorator(self)
    elif isinstance(self, Var):
        return convert_var(self)
    elif isinstance(self, TypeInfo):
        return convert_type_info(self, cfg)
    elif isinstance(self, TypeAlias):
        return convert_type_alias(self)
    elif isinstance(self, TypeVarExpr):
        return convert_type_var_expr(self)
    elif isinstance(self, ParamSpecExpr):
        return convert_param_spec_expr(self)
    elif isinstance(self, TypeVarTupleExpr):
        return convert_type_var_tuple_expr(self)
    return {"ERROR": f"{type(self)!r} unrecognized"}

