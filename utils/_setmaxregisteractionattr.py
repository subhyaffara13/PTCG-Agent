
def _setmaxregisteractionattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<action {str(x)}>', context=context)

