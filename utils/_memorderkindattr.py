
def _memorderkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mem_order<{str(x)}>', context=context)

