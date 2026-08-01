
def _rcproundingmodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvgpu<rcp_rounding_mode {str(x)}>', context=context)

