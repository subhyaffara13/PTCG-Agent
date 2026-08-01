
def _mmakindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_kind<{str(x)}>', context=context)

