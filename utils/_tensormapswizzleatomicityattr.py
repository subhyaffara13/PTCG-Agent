
def _tensormapswizzleatomicityattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tensormap_swizzle_atomicity<{str(x)}>', context=context)

