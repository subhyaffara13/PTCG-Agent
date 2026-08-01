
def _tensormapswizzleattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvgpu<swizzle {str(x)}>', context=context)

