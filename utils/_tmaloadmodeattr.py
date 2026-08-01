
def _tmaloadmodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tma_load_mode<{str(x)}>', context=context)

