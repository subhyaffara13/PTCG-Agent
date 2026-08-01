
def _mmafragattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mma_frag<{str(x)}>', context=context)

