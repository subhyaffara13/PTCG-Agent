
def _mmalayoutattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_layout<{str(x)}>', context=context)

