
def _mappingproxy_reduce(obj):
    return types.MappingProxyType, (dict(obj),)

