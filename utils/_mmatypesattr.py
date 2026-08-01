
def _mmatypesattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_type<{str(x)}>', context=context)

