
def _mmaintoverflowattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_int_overflow<{str(x)}>', context=context)

