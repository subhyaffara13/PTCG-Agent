
def _method_reduce(obj):
    return (types.MethodType, (obj.__func__, obj.__self__))

