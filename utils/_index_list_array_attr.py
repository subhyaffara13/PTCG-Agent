
def _indexListArrayAttr(x, context):
    return ArrayAttr.get([_i64ArrayAttr(v, context) for v in x])

