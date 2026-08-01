
def _tcgen05mmacollectoropattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_mma_collectorop<{str(x)}>', context=context)

