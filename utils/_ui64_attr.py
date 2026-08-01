
def _ui64Attr(x, context):
    return IntegerAttr.get(IntegerType.get_unsigned(64, context=context), x)

