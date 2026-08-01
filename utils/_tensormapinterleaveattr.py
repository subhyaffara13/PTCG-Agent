
def _tensormapinterleaveattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvgpu<interleave {str(x)}>', context=context)

