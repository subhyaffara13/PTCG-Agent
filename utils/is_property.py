
def is_property(defn: SymbolNode) -> bool:
    if isinstance(defn, FuncDef):
        return defn.is_property
    if isinstance(defn, Decorator):
        return defn.func.is_property
    if isinstance(defn, OverloadedFuncDef):
        if defn.items and isinstance(defn.items[0], Decorator):
            return defn.items[0].func.is_property
    return False

