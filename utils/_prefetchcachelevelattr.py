
def _prefetchcachelevelattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<prefetch_cache_level {str(x)}>', context=context)

