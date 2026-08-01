
def _wgmmascaleoutattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.wgmma_scale_out<{str(x)}>', context=context)

