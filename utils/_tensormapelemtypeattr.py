
def _tensormapelemtypeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tensormap_elemtype<{str(x)}>', context=context)

