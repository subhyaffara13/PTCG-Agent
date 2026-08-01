
def _si32Attr(x, context):
    return IntegerAttr.get(IntegerType.get_signed(32, context=context), x)

