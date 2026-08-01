
def _saturationmodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.sat_mode<{str(x)}>', context=context)

