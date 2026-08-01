
def _build_type_adapter(cls: type[_BaseUrl | _BaseMultiHostUrl]) -> TypeAdapter:
    return TypeAdapter(cls)

