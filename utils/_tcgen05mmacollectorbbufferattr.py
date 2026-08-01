
def _tcgen05mmacollectorbbufferattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_mma_collectorb<{str(x)}>', context=context)

