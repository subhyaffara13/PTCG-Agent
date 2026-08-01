
def find_method_names(defs: list[Statement]) -> set[str]:
    # TODO: Traverse into nested definitions
    result = set()
    for defn in defs:
        if isinstance(defn, FuncDef):
            result.add(defn.name)
        elif isinstance(defn, Decorator):
            result.add(defn.func.name)
        elif isinstance(defn, OverloadedFuncDef):
            for item in defn.items:
                result.update(find_method_names([item]))
    return result

