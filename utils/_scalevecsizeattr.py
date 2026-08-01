
def _scalevecsizeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.scale_vec_size<{str(x)}>', context=context)

