
def _is_decoratable(stub: nodes.SymbolNode) -> bool:
    if not isinstance(stub, nodes.TypeInfo):
        return False
    if stub.is_newtype:
        return False
    if stub.typeddict_type is not None:
        return all(
            name.isidentifier() and not keyword.iskeyword(name)
            for name in stub.typeddict_type.items.keys()
        )
    return True

