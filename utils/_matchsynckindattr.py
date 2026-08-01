
def _matchsynckindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<match_sync_kind {str(x)}>', context=context)

