
def _immutable_dict_flatten(d: immutable_dict[Any, _VT]) -> tuple[list[_VT], Context]:
    return _dict_flatten(d)

