
def _transform_recursive(
    data: object,
    *,
    annotation: type,
    inner_type: type | None = None,
) -> object:
    """Transform the given data against the expected type.

    Args:
        annotation: The direct type annotation given to the particular piece of data.
            This may or may not be wrapped in metadata types, e.g. `Required[T]`, `Annotated[T, ...]` etc

        inner_type: If applicable, this is the "inside" type. This is useful in certain cases where the outside type
            is a container type such as `List[T]`. In that case `inner_type` should be set to `T` so that each entry in
            the list can be transformed using the metadata from the container type.

            Defaults to the same value as the `annotation` argument.
    """
    from .._compat import model_dump

    if inner_type is None:
        inner_type = annotation

    stripped_type = strip_annotated_type(inner_type)
    origin = get_origin(stripped_type) or stripped_type
    if is_typeddict(stripped_type) and is_mapping(data):
        return _transform_typeddict(data, stripped_type)

    if origin == dict and is_mapping(data):
        items_type = get_args(stripped_type)[1]
        return {key: _transform_recursive(value, annotation=items_type) for key, value in data.items()}

    if (
        # List[T]
        (is_list_type(stripped_type) and is_list(data))
        # Iterable[T]
        or (is_iterable_type(stripped_type) and is_iterable(data) and not isinstance(data, str))
        # Sequence[T]
        or (is_sequence_type(stripped_type) and is_sequence(data) and not isinstance(data, str))
    ):
        # dicts are technically iterable, but it is an iterable on the keys of the dict and is not usually
        # intended as an iterable, so we don't transform it.
        if isinstance(data, dict):
            return cast(object, data)

        inner_type = extract_type_arg(stripped_type, 0)
        if _no_transform_needed(inner_type):
            # for some types there is no need to transform anything, so we can get a small
            # perf boost from skipping that work.
            #
            # but we still need to convert to a list to ensure the data is json-serializable
            if is_list(data):
                return data
            return list(data)

        return [_transform_recursive(d, annotation=annotation, inner_type=inner_type) for d in data]

    if is_union_type(stripped_type):
        # For union types we run the transformation against all subtypes to ensure that everything is transformed.
        #
        # TODO: there may be edge cases where the same normalized field name will transform to two different names
        # in different subtypes.
        for subtype in get_args(stripped_type):
            data = _transform_recursive(data, annotation=annotation, inner_type=subtype)
        return data

    if isinstance(data, pydantic.BaseModel):
        return model_dump(data, exclude_unset=True, mode="json", exclude=getattr(data, "__api_exclude__", None))

    annotated_type = _get_annotated_type(annotation)
    if annotated_type is None:
        return data

    # ignore the first argument as it is the actual type
    annotations = get_args(annotated_type)[1:]
    for annotation in annotations:
        if isinstance(annotation, PropertyInfo) and annotation.format is not None:
            return _format_data(data, annotation.format, annotation.format_template)

    return data

