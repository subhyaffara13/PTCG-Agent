
def _reductionkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<reduction_kind {str(x)}>', context=context)

