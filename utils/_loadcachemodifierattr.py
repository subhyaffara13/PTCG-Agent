
def _loadcachemodifierattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<load_cache_modifier {str(x)}>', context=context)

