from typing import Any

def _calculate_keys(
    self: BaseModel,
    include: MappingIntStrAny | None,
    exclude: MappingIntStrAny | None,
    exclude_unset: bool,
    update: dict[str, Any] | None = None,  # noqa UP006
) -> typing.AbstractSet[str] | None:
    if include is None and exclude is None and exclude_unset is False:
        return None

    keys: typing.AbstractSet[str]
    if exclude_unset:
        keys = self.__pydantic_fields_set__.copy()
    else:
        keys = set(self.__dict__.keys())
        keys = keys | (self.__pydantic_extra__ or {}).keys()

    if include is not None:
        keys &= include.keys()

    if update:
        keys -= update.keys()

    if exclude:
        keys -= {k for k, v in exclude.items() if _utils.ValueItems.is_true(v)}

    return keys

