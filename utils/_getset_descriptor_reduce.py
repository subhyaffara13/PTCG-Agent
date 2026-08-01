
def _getset_descriptor_reduce(obj):
    return getattr, (obj.__objclass__, obj.__name__)

