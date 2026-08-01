
def _proxykindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.proxy_kind<{str(x)}>', context=context)

