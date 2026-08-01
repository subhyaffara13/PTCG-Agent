
def _symbolRefAttr(x, context):
    if isinstance(x, list):
        return SymbolRefAttr.get(x, context=context)
    else:
        return FlatSymbolRefAttr.get(x, context=context)

