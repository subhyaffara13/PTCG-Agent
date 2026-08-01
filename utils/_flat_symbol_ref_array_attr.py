
def _flatSymbolRefArrayAttr(x, context):
    return ArrayAttr.get([_flatSymbolRefAttr(v, context) for v in x])

