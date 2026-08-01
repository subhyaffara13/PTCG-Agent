
def _tensormapfillmodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tensormap_fill_mode<{str(x)}>', context=context)

