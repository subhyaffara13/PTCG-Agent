
def get_func_def(typ: mypy.types.CallableType) -> SymbolNode | None:
    definition = typ.definition
    if isinstance(definition, Decorator):
        definition = definition.func
    return definition


def get_func_def(op: FuncDef | Decorator | OverloadedFuncDef) -> FuncDef:
    if isinstance(op, OverloadedFuncDef):
        assert op.impl
        op = op.impl
    if isinstance(op, Decorator):
        op = op.func
    return op

