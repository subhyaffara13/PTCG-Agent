
def _barrierreductionattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.reduction<{str(x)}>', context=context)

