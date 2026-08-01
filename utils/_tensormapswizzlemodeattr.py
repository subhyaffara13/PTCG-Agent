
def _tensormapswizzlemodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tensormap_swizzle_mode<{str(x)}>', context=context)

