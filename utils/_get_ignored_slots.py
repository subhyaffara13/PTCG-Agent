
def _get_ignored_slots(node: SymbolNode) -> tuple[str, ...]:
    if isinstance(node, OverloadedFuncDef):
        return ("setter",)
    if isinstance(node, TypeInfo):
        return ("special_alias",)
    return ()

