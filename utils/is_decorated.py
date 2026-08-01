
def is_decorated(builder: IRBuilder, fdef: FuncDef) -> bool:
    return fdef in builder.fdefs_to_decorators

