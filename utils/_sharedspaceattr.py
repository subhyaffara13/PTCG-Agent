
def _sharedspaceattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.shared_space<{str(x)}>', context=context)

