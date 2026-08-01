
def _extract_items(
    obj: object,
    path: Sequence[str],
    *,
    index: int,
    flattened_key: str | None,
    array_format: ArrayFormat,
) -> list[tuple[str, FileTypes]]:
    try:
        key = path[index]
    except IndexError:
        if not is_given(obj):
            # no value was provided - we can safely ignore
            return []

        # cyclical import
        from .._files import assert_is_file_content

        # We have exhausted the path, return the entry we found.
        assert flattened_key is not None

        if is_list(obj):
            files: list[tuple[str, FileTypes]] = []
            for array_index, entry in enumerate(obj):
                suffix = _array_suffix(array_format, array_index)
                emitted_key = (flattened_key + suffix) if flattened_key else suffix
                assert_is_file_content(entry, key=emitted_key)
                files.append((emitted_key, cast(FileTypes, entry)))
            return files

        assert_is_file_content(obj, key=flattened_key)
        return [(flattened_key, cast(FileTypes, obj))]

    index += 1
    if is_dict(obj):
        try:
            # Remove the field if there are no more dict keys in the path,
            # only "<array>" traversal markers or end.
            if all(p == "<array>" for p in path[index:]):
                item = obj.pop(key)
            else:
                item = obj[key]
        except KeyError:
            # Key was not present in the dictionary, this is not indicative of an error
            # as the given path may not point to a required field. We also do not want
            # to enforce required fields as the API may differ from the spec in some cases.
            return []
        if flattened_key is None:
            flattened_key = key
        else:
            flattened_key += f"[{key}]"
        return _extract_items(
            item,
            path,
            index=index,
            flattened_key=flattened_key,
            array_format=array_format,
        )
    elif is_list(obj):
        if key != "<array>":
            return []

        return flatten(
            [
                _extract_items(
                    item,
                    path,
                    index=index,
                    flattened_key=(
                        (flattened_key if flattened_key is not None else "") + _array_suffix(array_format, array_index)
                    ),
                    array_format=array_format,
                )
                for array_index, item in enumerate(obj)
            ]
        )

    # Something unexpected was passed, just ignore it.
    return []

