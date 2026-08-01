
def _listify(obj):
    if obj is None:
        return []
    elif isinstance(obj, str):
        return [obj]
    else:
        return obj

