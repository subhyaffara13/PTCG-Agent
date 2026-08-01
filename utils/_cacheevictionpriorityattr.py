
def _cacheevictionpriorityattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<cache_eviction_priority {str(x)}>', context=context)

