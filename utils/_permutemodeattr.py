
def _permutemodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.permute_mode<{str(x)}>', context=context)

