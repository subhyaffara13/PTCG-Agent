
def _typed_map_converter(
    init_val: Mapping[str, Callable[[TypeChecker, Any], bool]],
) -> HashTrieMap[str, Callable[[TypeChecker, Any], bool]]:
    return HashTrieMap.convert(init_val)

