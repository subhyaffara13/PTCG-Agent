
def _tcgen05waitkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_wait<{str(x)}>', context=context)

