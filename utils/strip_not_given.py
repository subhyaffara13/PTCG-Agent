
def strip_not_given(obj: None) -> None: ...


def strip_not_given(obj: Mapping[_K, _V | NotGiven]) -> dict[_K, _V]: ...


def strip_not_given(obj: object) -> object: ...


def strip_not_given(obj: object | None) -> object:
    """Remove all top-level keys where their values are instances of `NotGiven`"""
    if obj is None:
        return None

    if not is_mapping(obj):
        return obj

    return {key: value for key, value in obj.items() if not isinstance(value, NotGiven)}

