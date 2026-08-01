
def _tcgen05fencekindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_fence<{str(x)}>', context=context)

