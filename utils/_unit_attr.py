
def _unitAttr(x, context):
    if x:
        return UnitAttr.get(context=context)
    else:
        return None

