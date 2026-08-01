
def _tpu_reductionkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.reduction_kind<{str(x)}>', context=context)

