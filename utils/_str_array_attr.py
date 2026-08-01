
def _strArrayAttr(x, context):
    return ArrayAttr.get([_stringAttr(v, context) for v in x])

