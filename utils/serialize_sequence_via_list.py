from typing import Any

def serialize_sequence_via_list(
    v: Any, handler: core_schema.SerializerFunctionWrapHandler, info: core_schema.SerializationInfo
) -> Any:
    items: list[Any] = []

    mapped_origin = SEQUENCE_ORIGIN_MAP.get(type(v), None)
    if mapped_origin is None:
        # we shouldn't hit this branch, should probably add a serialization error or something
        return v

    for index, item in enumerate(v):
        try:
            v = handler(item, index)
        except PydanticOmit:  # noqa: PERF203
            pass
        else:
            items.append(v)

    if info.mode_is_json():
        return items
    else:
        return mapped_origin(items)

