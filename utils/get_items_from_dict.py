from typing import Any

def get_items_from_dict(obj: dict[K, V]) -> Iterable[tuple[K, V | Any]]:
    # Get items without calling the user defined __getitem__ or keys method.
    assert isinstance(obj, dict)
    if istype(obj, (dict, OrderedDict)):
        return obj.items()
    elif isinstance(obj, OrderedDict):
        return [(k, OrderedDict.__getitem__(obj, k)) for k in OrderedDict.keys(obj)]
    else:
        return [(k, dict.__getitem__(obj, k)) for k in dict.keys(obj)]

