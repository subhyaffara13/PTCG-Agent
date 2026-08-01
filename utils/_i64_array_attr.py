
def _i64ArrayAttr(x, context):
    return ArrayAttr.get([_i64Attr(v, context) for v in x])

