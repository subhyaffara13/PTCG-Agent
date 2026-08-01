
def _symbolRefArrayAttr(x, context):
    return ArrayAttr.get([_symbolRefAttr(v, context) for v in x])

