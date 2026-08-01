
def _tpu_roundingmodeenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.rounding_mode<{str(x)}>', context=context)

