
def _wgmmatypesattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.wgmma_type<{str(x)}>', context=context)

