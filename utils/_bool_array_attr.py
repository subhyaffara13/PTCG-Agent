
def _boolArrayAttr(x, context):
    return ArrayAttr.get([_boolAttr(v, context) for v in x])

