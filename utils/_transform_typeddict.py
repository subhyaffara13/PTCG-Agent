
def _transform_typeddict(
    data: Mapping[str, object],
    expected_type: type,
) -> Mapping[str, object]:
    result: dict[str, object] = {}
    annotations = get_type_hints(expected_type, include_extras=True)
    for key, value in data.items():
        if not is_given(value):
            # we don't need to include omitted values here as they'll
            # be stripped out before the request is sent anyway
            continue

        type_ = annotations.get(key)
        if type_ is None:
            # we do not have a type annotation for this field, leave it as is
            result[key] = value
        else:
            result[_maybe_transform_key(key, type_)] = _transform_recursive(value, annotation=type_)
    return result

