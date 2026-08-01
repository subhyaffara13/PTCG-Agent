
def _tmareduxkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tma_redux_kind<{str(x)}>', context=context)

