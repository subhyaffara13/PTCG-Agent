
def _f32ArrayAttr(x, context):
    return ArrayAttr.get([_f32Attr(v, context) for v in x])

