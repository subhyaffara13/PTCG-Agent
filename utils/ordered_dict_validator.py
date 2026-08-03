from typing import Any

def ordered_dict_validator(v: Any) -> 'AnyOrderedDict':
    if isinstance(v, OrderedDict):
        return v

    try:
        return OrderedDict(v)
    except (TypeError, ValueError):
        raise errors.DictError()

