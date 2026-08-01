
def is_mapping(value: nodes.NodeNG) -> bool:
    return _supports_protocol(value, _supports_mapping_protocol)


def is_mapping(obj: object) -> TypeGuard[Mapping[str, object]]:
    return isinstance(obj, Mapping)

