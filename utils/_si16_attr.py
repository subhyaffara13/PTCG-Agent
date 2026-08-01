
def _si16Attr(x, context):
    return IntegerAttr.get(IntegerType.get_signed(16, context=context), x)

