
def _si8Attr(x, context):
    return IntegerAttr.get(IntegerType.get_signed(8, context=context), x)

