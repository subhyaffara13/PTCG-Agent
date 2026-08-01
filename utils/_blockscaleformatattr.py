
def _blockscaleformatattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.block_scale_format<{str(x)}>', context=context)

