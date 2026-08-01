
def _nvvmmemoryspaceattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.memory_space<{str(x)}>', context=context)

