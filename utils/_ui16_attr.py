
def _ui16Attr(x, context):
    return IntegerAttr.get(IntegerType.get_unsigned(16, context=context), x)

