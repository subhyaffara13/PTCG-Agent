
def _i32ArrayAttr(x, context):
    return ArrayAttr.get([_i32Attr(v, context) for v in x])

