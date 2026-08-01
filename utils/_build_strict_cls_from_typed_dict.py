
def _build_strict_cls_from_typed_dict(schema: type[TypedDictType]) -> Type:
    # Extract type hints from the TypedDict class
    type_hints = _get_typed_dict_annotations(schema)

    # If the TypedDict is not total, wrap fields as NotRequired (unless explicitly Required or NotRequired)
    if not getattr(schema, "__total__", True):
        for key, value in type_hints.items():
            origin = get_origin(value)

            if origin is Annotated:
                base, *meta = get_args(value)
                if not _is_required_or_notrequired(base):
                    base = NotRequired[base]
                type_hints[key] = Annotated[tuple([base] + list(meta))]  # type: ignore
            elif not _is_required_or_notrequired(value):
                type_hints[key] = NotRequired[value]

    # Convert type hints to dataclass fields
    fields = []
    for key, value in type_hints.items():
        if get_origin(value) is Annotated:
            base, *meta = get_args(value)
            fields.append((key, base, field(default=_TYPED_DICT_DEFAULT_VALUE, metadata={"validator": meta[0]})))
        else:
            fields.append((key, value, field(default=_TYPED_DICT_DEFAULT_VALUE)))

    # Create a strict dataclass from the TypedDict fields
    return strict(make_dataclass(schema.__name__, fields))

