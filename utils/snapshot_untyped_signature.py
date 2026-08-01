
def snapshot_untyped_signature(func: OverloadedFuncDef | FuncItem) -> SymbolSnapshot:
    """Create a snapshot of the signature of a function that has no explicit signature.

    If the arguments to a function without signature change, it must be
    considered as different. We have this special casing since we don't store
    the implicit signature anywhere, and we'd rather not construct new
    Callable objects in this module (the idea is to only read properties of
    the AST here).
    """
    if isinstance(func, FuncItem):
        return (tuple(func.arg_names), tuple(func.arg_kinds))
    else:
        result: list[SymbolSnapshot] = []
        for item in func.items:
            if isinstance(item, Decorator):
                if item.var.type:
                    result.append(snapshot_type(item.var.type))
                else:
                    result.append(("DecoratorWithoutType",))
            else:
                result.append(snapshot_untyped_signature(item))
        return tuple(result)

