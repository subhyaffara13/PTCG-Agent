
def _tcgen05mmablockscaleattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_mma_block_scale<{str(x)}>', context=context)

