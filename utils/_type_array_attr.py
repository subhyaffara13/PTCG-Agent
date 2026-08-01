
def _typeArrayAttr(x, context):
    return _arrayAttr([TypeAttr.get(t, context=context) for t in x], context)

