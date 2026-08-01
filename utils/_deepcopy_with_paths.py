
def _deepcopy_with_paths(item: _T, paths: Sequence[Sequence[str]], index: int) -> _T:
    if not paths:
        return item
    if is_mapping(item):
        key_to_paths: dict[str, list[Sequence[str]]] = {}
        for path in paths:
            if index < len(path):
                key_to_paths.setdefault(path[index], []).append(path)

        # if no path continues through this mapping, it won't be mutated and copying it is redundant
        if not key_to_paths:
            return item

        result = dict(item)
        for key, subpaths in key_to_paths.items():
            if key in result:
                result[key] = _deepcopy_with_paths(result[key], subpaths, index + 1)
        return cast(_T, result)
    if is_list(item):
        array_paths = [path for path in paths if index < len(path) and path[index] == "<array>"]

        # if no path expects a list here, nothing will be mutated inside it - return by reference
        if not array_paths:
            return cast(_T, item)
        return cast(_T, [_deepcopy_with_paths(entry, array_paths, index + 1) for entry in item])
    return item

