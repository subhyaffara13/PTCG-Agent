
def _mmab1opattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_b1op<{str(x)}>', context=context)

