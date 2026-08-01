
def _shflkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<shfl_kind {str(x)}>', context=context)

