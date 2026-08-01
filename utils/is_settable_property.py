
def is_settable_property(defn: SymbolNode | None) -> TypeGuard[OverloadedFuncDef]:
    if isinstance(defn, OverloadedFuncDef):
        if defn.items and isinstance(defn.items[0], Decorator):
            return defn.items[0].func.is_property
    return False

