
def _gpu_addressspaceattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu.address_space<{str(x)}>', context=context)

