
def _affineMapArrayAttr(x, context):
    return ArrayAttr.get([_affineMapAttr(v, context) for v in x])

