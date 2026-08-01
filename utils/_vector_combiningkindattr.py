
def _vector_combiningkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#vector.kind<{str(x)}>', context=context)

