
def _f64ArrayAttr(x, context):
    return ArrayAttr.get([_f64Attr(v, context) for v in x])

