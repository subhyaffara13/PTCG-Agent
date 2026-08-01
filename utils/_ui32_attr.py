
def _ui32Attr(x, context):
    return IntegerAttr.get(IntegerType.get_unsigned(32, context=context), x)

