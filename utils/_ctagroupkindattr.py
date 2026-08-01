
def _ctagroupkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.cta_group<{str(x)}>', context=context)

