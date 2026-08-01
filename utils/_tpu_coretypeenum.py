
def _tpu_coretypeenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.core_type<{str(x)}>', context=context)

