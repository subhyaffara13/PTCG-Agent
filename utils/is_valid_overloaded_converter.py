
def is_valid_overloaded_converter(defn: OverloadedFuncDef) -> bool:
    return all(
        (not isinstance(item, Decorator) or isinstance(item.func.type, FunctionLike))
        for item in defn.items
    )

