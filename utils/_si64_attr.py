
def _si64Attr(x, context):
    return IntegerAttr.get(IntegerType.get_signed(64, context=context), x)

