
def _tcgen05mmakindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_mma_kind<{str(x)}>', context=context)

