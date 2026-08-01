
def _votesynckindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<vote_sync_kind {str(x)}>', context=context)

