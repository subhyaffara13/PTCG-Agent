
def _tmastoremodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tma_store_mode<{str(x)}>', context=context)

