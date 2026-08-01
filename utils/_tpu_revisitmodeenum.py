
def _tpu_revisitmodeenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.revisit_mode<{str(x)}>', context=context)

