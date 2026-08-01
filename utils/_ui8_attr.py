
def _ui8Attr(x, context):
    return IntegerAttr.get(IntegerType.get_unsigned(8, context=context), x)

