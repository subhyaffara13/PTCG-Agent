
def _dictArrayAttr(x, context):
    return ArrayAttr.get([_dictAttr(v, context) for v in x])

