
def _tpu_packformatenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.pack_format<{str(x)}>', context=context)

