
def _mmablockscalekindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.block_scale_kind<{str(x)}>', context=context)

