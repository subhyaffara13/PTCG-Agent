
def _wgmmascaleinattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.wgmma_scale_in<{str(x)}>', context=context)

